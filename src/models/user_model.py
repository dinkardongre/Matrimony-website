from sqlalchemy import (Column, Integer, String, Boolean, Date, ForeignKey, Text, DateTime, Float, UniqueConstraint)
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    username = Column(String, nullable=False)
    hash_password = Column(String(255), nullable=False)
    otp = Column(String, nullable=True, default=None)
    date_of_birth = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    profile = relationship("Profile", back_populates="user", uselist=False)
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    likes_sent = relationship("Like", foreign_keys='Like.liker_id', back_populates="liker")
    likes_received = relationship("Like", foreign_keys='Like.liked_id', back_populates="liked")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    religion = Column(String(50))
    caste = Column(String(50))
    occupation = Column(String(100))
    education = Column(String(100))
    city = Column(String(100))
    bio = Column(Text)
    photo_url = Column(String(255))

    user = relationship("User", back_populates="profile")


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(Float, default=0.0)
    duration_days = Column(Integer, default=30)

    message_limit = Column(Integer, default=20)
    like_limit = Column(Integer, default=30)
    contact_view_limit = Column(Integer, default=10)
    can_video_call = Column(Boolean, default=False)
    can_priority_listing = Column(Boolean, default=False)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)
    start_date = Column(DateTime, default=datetime)
    end_date = Column(DateTime)
    remaining_messages = Column(Integer)
    remaining_likes = Column(Integer)
    remaining_contacts = Column(Integer)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="subscription")
    plan = relationship("SubscriptionPlan")

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    liker_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    liked_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime)

    __table_args__ = (UniqueConstraint("liker_id", "liked_id", name="_unique_like_pair"),)

    liker = relationship("User", foreign_keys=[liker_id], back_populates="likes_sent")
    liked = relationship("User", foreign_keys=[liked_id], back_populates="likes_received")