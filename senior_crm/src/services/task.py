from typing import Sequence
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundError, ForbiddenError, ValidationError
from src.repositories import TaskRepository, DealRepository, ActivityRepository
from src.models import Task, User, UserRole
from src.services.organization import OrganizationService


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TaskRepository(session)
        self.deal_repo = DealRepository(session)
        self.activity_repo = ActivityRepository(session)
        self.org_service = OrganizationService(session)

    async def get_tasks(
        self,
        organization_id: int,
        user: User,
        deal_id: int | None = None,
        only_open: bool = False,
        due_before: datetime | None = None,
        due_after: datetime | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Sequence[Task]:
        """Get tasks for organization or specific deal."""
        await self.org_service.get_membership(organization_id, user)

        if deal_id:
            # Validate deal belongs to organization
            deal = await self.deal_repo.get_by_id(deal_id)
            if not deal or deal.organization_id != organization_id:
                raise NotFoundError("Deal not found")

            return await self.repo.get_by_deal(
                deal_id, only_open=only_open, due_before=due_before, due_after=due_after
            )

        skip = (page - 1) * page_size
        return await self.repo.get_by_organization(
            organization_id,
            only_open=only_open,
            due_before=due_before,
            due_after=due_after,
            skip=skip,
            limit=page_size,
        )

    async def get_task(
        self,
        task_id: int,
        organization_id: int,
        user: User,
    ) -> Task:
        """Get single task by ID."""
        await self.org_service.get_membership(organization_id, user)

        task = await self.repo.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")

        # Validate task's deal belongs to organization
        deal = await self.deal_repo.get_by_id(task.deal_id)
        if not deal or deal.organization_id != organization_id:
            raise NotFoundError("Task not found")

        return task

    async def create_task(
        self,
        organization_id: int,
        user: User,
        deal_id: int,
        title: str,
        due_date: datetime,
        description: str | None = None,
    ) -> Task:
        """Create new task for a deal."""
        member = await self.org_service.get_membership(organization_id, user)

        # Validate deal belongs to organization
        deal = await self.deal_repo.get_by_id(deal_id)
        if not deal or deal.organization_id != organization_id:
            raise NotFoundError("Deal not found")

        # Rule: Members can only create tasks for their own deals
        if member.role == UserRole.MEMBER and deal.owner_id != user.id:
            raise ForbiddenError("You can only create tasks for your own deals")

        # Rule: due_date cannot be in the past
        self._validate_due_date(due_date)

        task = await self.repo.create(
            deal_id=deal_id,
            title=title,
            description=description,
            due_date=due_date,
            is_done=False,
        )

        # Create activity for task creation
        await self.activity_repo.create_task_created(
            deal_id=deal_id,
            author_id=user.id,
            task_id=task.id,
            task_title=title,
        )

        await self.session.commit()
        return task

    async def update_task(
        self,
        task_id: int,
        organization_id: int,
        user: User,
        title: str | None = None,
        description: str | None = None,
        due_date: datetime | None = None,
        is_done: bool | None = None,
    ) -> Task:
        """Update task."""
        member = await self.org_service.get_membership(organization_id, user)

        task = await self.repo.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")

        deal = await self.deal_repo.get_by_id(task.deal_id)
        if not deal or deal.organization_id != organization_id:
            raise NotFoundError("Task not found")

        # Members can only update tasks for their own deals
        if member.role == UserRole.MEMBER and deal.owner_id != user.id:
            raise ForbiddenError("You can only update tasks for your own deals")

        # Validate due_date if provided
        if due_date is not None:
            self._validate_due_date(due_date)

        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if due_date is not None:
            update_data["due_date"] = due_date
        if is_done is not None:
            update_data["is_done"] = is_done

        task = await self.repo.update(task, **update_data)
        await self.session.commit()
        return task

    async def delete_task(
        self,
        task_id: int,
        organization_id: int,
        user: User,
    ) -> None:
        """Delete task."""
        member = await self.org_service.get_membership(organization_id, user)

        task = await self.repo.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")

        deal = await self.deal_repo.get_by_id(task.deal_id)
        if not deal or deal.organization_id != organization_id:
            raise NotFoundError("Task not found")

        # Members can only delete tasks for their own deals
        if member.role == UserRole.MEMBER and deal.owner_id != user.id:
            raise ForbiddenError("You can only delete tasks for your own deals")

        await self.repo.delete(task)
        await self.session.commit()

    def _validate_due_date(self, due_date: datetime) -> None:
        """Validate that due_date is not in the past."""
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        if due_date < today:
            raise ValidationError("Due date cannot be in the past")
