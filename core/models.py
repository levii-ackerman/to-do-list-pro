from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
from core.database import Base
from datetime import datetime, timezone
# from schemas import TaskStatus

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    email = Column(String(30), unique=True, index=True)
    full_name = Column(String(50))
    password = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tasks = relationship('Task', back_populates='user')
    friends = relationship('Friend', foreign_keys='Friend.user_id', back_populates='user')
    group_owner = relationship('Group', back_populates='owner')
    group_task_assignments = relationship('GroupTaskAssignment', back_populates='user')
    notifications = relationship('Notification', back_populates='user')
    comments = relationship('Comment', back_populates='user')


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # status = Column(Enum(TaskStatus, create_type=True), default=TaskStatus.pending, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='tasks')
    notifications = relationship('Notification', back_populates='task')
    comments = relationship('Comment', back_populates='task')


class Friend(Base):
    __tablename__ = 'friend'
    __table_args__ = (UniqueConstraint('user_id', 'friend_id', name='uq_friend_pair'),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    friend_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', foreign_keys=[user_id], back_populates='friends')
    friend = relationship('User', foreign_keys=[friend_id])


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship('User', back_populates='group_owner')
    tasks = relationship('GroupTask', back_populates='group')


class GroupMember(Base):
    __tablename__ = 'group_member'
    __table_args__ = (UniqueConstraint('user_id', 'group_id', name='uq_user_group'),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    group_id = Column(Integer, ForeignKey('group.id'))


class GroupTask(Base):
    __tablename__ = 'group_task'
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=False)
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    group_id = Column(Integer, ForeignKey('group.id'))
    group = relationship('Group', back_populates='tasks')
    assignments = relationship('GroupTaskAssignment', back_populates='task')


class GroupTaskAssignment(Base):
    __tablename__ = 'group_task_assignment'
    __table_args__ = (UniqueConstraint('user_id', 'task_id', name='uq_task_user'),)

    id = Column(Integer, primary_key=True)
    is_completed = Column(Boolean, default=False)
    assigned_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    user_id = Column(Integer, ForeignKey('user.id'))
    task_id = Column(Integer, ForeignKey('group_task.id'))

    user = relationship('User', back_populates='group_task_assignments')
    task = relationship('GroupTask', back_populates='assignments')


class Notification(Base):
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True)
    message = Column(String(50), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user_id = Column(Integer, ForeignKey('user.id'))
    task_id = Column(Integer, ForeignKey('task.id'))

    user = relationship('User', back_populates='notifications')
    task = relationship('Task', back_populates='notifications')


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user_id = Column(Integer, ForeignKey('user.id'))
    task_id = Column(Integer, ForeignKey('task.id'))

    user = relationship('User', back_populates='comments')
    task = relationship('Task', back_populates='comments')
