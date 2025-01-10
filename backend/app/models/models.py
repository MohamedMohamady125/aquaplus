# coding: utf-8
from sqlalchemy import BINARY, CHAR, CheckConstraint, Column, DECIMAL, Date, DateTime, Enum, ForeignKey, Index, Integer, JSON, String, TIMESTAMP, Text, VARBINARY, text, Numeric
from sqlalchemy.dialects.mysql import ENUM, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from decimal import Decimal

Base = declarative_base()
metadata = Base.metadata


class Item(Base):
    __tablename__ = 'items'
    __table_args__ = (
        Index('idx_type_brand', 'type', 'brand'),
    )

    item_id = Column(Integer, primary_key=True)
    type = Column(VARCHAR(50), nullable=False, index=True)
    brand = Column(VARCHAR(50), nullable=False, index=True)
    color = Column(VARCHAR(50), nullable=False)
    size = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, index=True, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Location(Base):
    __tablename__ = 'locations'

    location_id = Column(Integer, primary_key=True)
    governorate = Column(String(255), nullable=False, index=True)
    city = Column(String(255), nullable=False, index=True)
    neighborhood = Column(String(255), index=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        CheckConstraint('((`is_deleted` = 0) or (`deleted_at` is not null))'),
        Index('idx_role_location', 'role', 'main_location'),
        Index('idx_user_id_status', 'user_id', 'account_status')
    )

    user_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    recovery_email = Column(String(50))
    preferred_language = Column(Enum('ar', 'en'), server_default=text("'en'"))
    gender = Column(Enum('male', 'female'))
    date_of_birth = Column(Date)
    phone_number = Column(CHAR(15))
    backup_phone = Column(CHAR(15))
    role = Column(Enum('swimmer or parent', 'coach', 'academy', 'event_organizer', 'support_agent', 'admin', 'vendor'))
    profile_photo_url = Column(String(255))
    account_status = Column(Enum('active', 'inactive', 'suspended', 'banned'), nullable=False, server_default=text("'active'"))
    main_location = Column(String(50))
    ban_reason = Column(String(255))
    user_name = Column(String(20), nullable=False, unique=True)
    password_hash = Column(CHAR(64), nullable=False)
    salt = Column(CHAR(32), nullable=False)
    last_login_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    deleted_at = Column(TIMESTAMP)
    is_deleted = Column(TINYINT(1), server_default=text("'0'"))


class UserCommissionRate(Base):
    __tablename__ = 'user_commission_rates'
    __table_args__ = (
        CheckConstraint('((`commission_rate` >= 0) and (`commission_rate` <= 100))'),
        Index('idx_role_id', 'commission_rate_id', 'role')
    )

    commission_rate_id = Column(Integer, primary_key=True)
    role = Column(Enum('coach', 'swimmer', 'academy', 'vendor', 'event_orgainzer'), nullable=False)
    commission_rate = Column(DECIMAL(5, 2), nullable=False, index=True)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class VendorSubscription(Base):
    __tablename__ = 'vendor_subscriptions'
    __table_args__ = (
        CheckConstraint('(`price` >= 0)'),
        Index('idx_subscription_dates', 'start_date', 'end_date'),
        Index('idx_vendor_subs_id', 'subscription_id', 'status')
    )

    subscription_id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum('active', 'cancelled', 'expired'), server_default=text("'active'"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class PasswordResetToken(Base):
    __tablename__ = 'PasswordResetToken'
    __table_args__ = (
        Index('idx_status_expires', 'status', 'expires_at'),
    )

    prt_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    token = Column(BINARY(32), nullable=False, unique=True)
    expires_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    used_at = Column(TIMESTAMP)
    ip_address = Column(VARBINARY(16))
    status = Column(Enum('active', 'expired', 'used'), server_default=text("'active'"))
    is_deleted = Column(TINYINT(1), server_default=text("'0'"))

    user = relationship('User')


class Academy(Base):
    __tablename__ = 'academy'
    __table_args__ = (
        CheckConstraint('(`coach_count` >= 0)'),
        Index('idx_academy_id_specialty', 'academy_id', 'specialty')
    )

    academy_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    specialty = Column(Enum('swimming', 'fitness'))
    coach_count = Column(Integer)
    main_location_url = Column(String(255))
    business_license_url = Column(String(255))
    tax_number = Column(String(50))
    contact_email = Column(String(50))
    website_url = Column(String(255))
    contact_phone_number = Column(String(15))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    main_location = Column(String(20), nullable=False, index=True)

    user = relationship('User')


class Coach(Base):
    __tablename__ = 'coach'
    __table_args__ = (
        CheckConstraint('(`experience_years` >= 0)'),
        CheckConstraint('(`experience_years` >= 0)')
    )

    coach_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    speciality = Column(Enum('swimming', 'fitness', 'both'), nullable=False, index=True)
    experience_years = Column(Integer, server_default=text("'0'"))
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User')


class CommissionTransaction(Base):
    __tablename__ = 'commission_transaction'
    __table_args__ = (
        CheckConstraint('(`commission_amount` >= 0)'),
        CheckConstraint('(`transaction_amount` >= 0)'),
        Index('idx_user_transaction', 'user_id', 'transaction_id')
    )

    transaction_id = Column(Integer, primary_key=True)
    commission_rate_id = Column(ForeignKey('user_commission_rates.commission_rate_id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    transaction_amount = Column(DECIMAL(10, 2), nullable=False)
    commission_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum('pending', 'paid', 'failed', 'refunded'), index=True, server_default=text("'pending'"))
    description = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    commission_rate = relationship('UserCommissionRate')
    user = relationship('User')


class Email(Base):
    __tablename__ = 'emails'
    __table_args__ = (
        Index('idx_receiver_read_status', 'receiver_id', 'read_status'),
    )

    email_id = Column(Integer, primary_key=True)
    receiver_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    subject = Column(String(255, 'utf8mb4_general_ci'), nullable=False)
    body = Column(Text(collation='utf8mb4_general_ci'), nullable=False)
    attachments = Column(JSON)
    sent_at = Column(DateTime, index=True, server_default=text("CURRENT_TIMESTAMP"))
    sent_status = Column(ENUM('sent', 'failed'), server_default=text("'failed'"))
    read_status = Column(ENUM('read', 'unread'), server_default=text("'unread'"))

    receiver = relationship('User')


class EventOrganizer(Base):
    __tablename__ = 'event_organizer'

    organizer_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User')


class FamilyGroup(Base):
    __tablename__ = 'family_groups'

    family_id = Column(Integer, primary_key=True)
    primary_user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    family_name = Column(String(100), server_default=text("'My Family'"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # Keep the existing relationship with User
    primary_user = relationship('User')
    # Add the relationship with FamilyMember
    members = relationship('FamilyMember', back_populates='family_group', cascade="all, delete-orphan")


class MarketingService(Base):
    __tablename__ = 'marketing_services'
    __table_args__ = (
        CheckConstraint('(`price` >= 0)'),
        Index('idx_user_service', 'user_id', 'status')
    )

    mst_id = Column(Integer, primary_key=True)
    service_name = Column(String(100), nullable=False)
    user_id = Column(ForeignKey('user.user_id'), nullable=False)
    platform = Column(Enum('snapchat', 'instagram', 'facebook', 'twitter', 'tiktok', 'other'), nullable=False)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    status = Column(Enum('active', 'inactive', 'archived'), server_default=text("'active'"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User')


class MarketplaceListing(Base):
    __tablename__ = 'marketplace_listings'
    __table_args__ = (
        CheckConstraint('(`price` >= 0)'),
    )

    listing_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    item_id = Column(ForeignKey('items.item_id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(String(255, 'utf8mb4_general_ci'), nullable=False)
    photos = Column(JSON, nullable=False)
    gender = Column(ENUM('male', 'female', 'unisex'))
    description = Column(Text(collation='utf8mb4_general_ci'))
    payment_type = Column(ENUM('none', 'in_app', 'vendor_managed'), nullable=False, server_default=text("'none'"))
    price = Column(DECIMAL(10, 2), nullable=False, index=True)
    item_condition = Column(ENUM('new', 'used'), nullable=False)
    shipping_available = Column(TINYINT(1), server_default=text("'0'"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    item = relationship('Item')
    user = relationship('User')


class Notification(Base):
    __tablename__ = 'notifications'
    __table_args__ = (
        Index('idx_receiver_read_status', 'receiver_id', 'read_status'),
    )

    notification_id = Column(Integer, primary_key=True)
    receiver_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(String(255, 'utf8mb4_general_ci'), nullable=False)
    description = Column(Text(collation='utf8mb4_general_ci'), nullable=False)
    sent_at = Column(DateTime, index=True, server_default=text("CURRENT_TIMESTAMP"))
    read_status = Column(ENUM('read', 'unread'), server_default=text("'unread'"))

    receiver = relationship('User')


class Photographer(Base):
    __tablename__ = 'photographer'

    photographer_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    deleted_at = Column(TIMESTAMP)

    user = relationship('User')


class SellerReview(Base):
    __tablename__ = 'seller_reviews'
    __table_args__ = (
        CheckConstraint('(`rating` between 1 and 5)'),
        CheckConstraint('(`rating` between 1 and 5)'),
        Index('idx_seller_rating', 'seller_id', 'rating')
    )

    review_id = Column(Integer, primary_key=True)
    seller_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    buyer_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    rating = Column(TINYINT, nullable=False)
    average_rating = Column(DECIMAL(3, 2))
    feedback = Column(Text(collation='utf8mb4_general_ci'))
    created_at = Column(TIMESTAMP, index=True, server_default=text("CURRENT_TIMESTAMP"))

    buyer = relationship('User', primaryjoin='SellerReview.buyer_id == User.user_id')
    seller = relationship('User', primaryjoin='SellerReview.seller_id == User.user_id')


class Sm(Base):
    __tablename__ = 'sms'
    __table_args__ = (
        Index('idx_receiver_delivery_status', 'receiver_id', 'delivery_status'),
    )

    sms_id = Column(Integer, primary_key=True)
    receiver_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    message = Column(Text(collation='utf8mb4_general_ci'), nullable=False)
    sent_at = Column(DateTime, index=True, server_default=text("CURRENT_TIMESTAMP"))
    sent_status = Column(ENUM('pending', 'sent', 'failed'), server_default=text("'pending'"))
    delivery_status = Column(ENUM('pending', 'delivered', 'failed'), server_default=text("'pending'"))

    receiver = relationship('User')


class SupportAgent(Base):
    __tablename__ = 'support_agent'

    agent_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, unique=True)
    department = Column(ENUM('support', 'technical', 'billing', 'sales'), server_default=text("'support'"))
    status = Column(ENUM('active', 'inactive', 'suspended'), index=True, server_default=text("'active'"))
    active = Column(TINYINT(1), nullable=False, index=True, server_default=text("'1'"))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User')


class Swimmer(Base):
    __tablename__ = 'swimmer'
    __table_args__ = (
        Index('idx_skill_created', 'skill_level', 'created_at'),
    )

    swimmer_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    skill_level = Column(Enum('beginner', 'intermediate', 'advanced'), nullable=False, index=True)
    created_at = Column(TIMESTAMP, index=True, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    goals = Column(String(150))

    user = relationship('User')


class UserVerification(Base):
    __tablename__ = 'user_verification'

    verification_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    verification_type = Column(Enum('email', 'phone'), nullable=False)
    verification_code = Column(String(6), nullable=False)
    is_verified = Column(TINYINT(1), server_default=text("'0'"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    expires_at = Column(TIMESTAMP, nullable=False)

    user = relationship('User')


class Vendor(Base):
    __tablename__ = 'vendor'

    vendor_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, unique=True)
    can_ship = Column(TINYINT(1), index=True, server_default=text("'0'"))
    description = Column(Text)
    status = Column(Enum('active', 'inactive', 'suspended'), server_default=text("'active'"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User')


class CoachCertification(Base):
    __tablename__ = 'coach_certification'
    __table_args__ = (
        Index('idx_coach_created', 'coach_id', 'created_at'),
    )

    certification_id = Column(Integer, primary_key=True)
    coach_id = Column(ForeignKey('coach.coach_id', ondelete='CASCADE'), nullable=False, index=True)
    image_url = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    coach = relationship('Coach')


class CoachIdentification(Base):
    __tablename__ = 'coach_identification'
    __table_args__ = (
        Index('idx_coach_created', 'coach_id', 'created_at'),
    )

    identification_id = Column(Integer, primary_key=True)
    coach_id = Column(ForeignKey('coach.coach_id', ondelete='CASCADE'), nullable=False, index=True)
    image_url = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    coach = relationship('Coach')


class Commission(Base):
    __tablename__ = 'commissions'
    __table_args__ = (
        CheckConstraint('((`customer_fee_rate` >= 0) and (`customer_fee_rate` <= 100))'),
        CheckConstraint('((`default_rate` >= 0) and (`default_rate` <= 100))'),
        Index('idx_user_type_status', 'user_type', 'status'),
        Index('idx_active_dates', 'active_from', 'active_to'),
        Index('idx_vendor_user_type_status', 'vendor_id', 'user_type', 'status')
    )

    commission_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    vendor_id = Column(ForeignKey('vendor.vendor_id', ondelete='CASCADE'))
    commission_type = Column(Enum('coach', 'academy', 'event_organizer', 'vendor', 'customer'), nullable=False)
    user_type = Column(Enum('coach', 'academy', 'event_organizer'))
    default_rate = Column(DECIMAL(4, 2), nullable=False)
    customer_fee_rate = Column(DECIMAL(4, 2), nullable=False)
    amount = Column(DECIMAL(10, 2))
    active_from = Column(Date, nullable=False)
    active_to = Column(Date)
    status = Column(Enum('active', 'inactive'), server_default=text("'active'"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User')
    vendor = relationship('Vendor')


class Event(Base):
    __tablename__ = 'event'
    __table_args__ = (
        CheckConstraint('(`price` >= 0)'),
        Index('idx_location_specialty', 'location_id', 'specialty')
    )

    event_id = Column(Integer, primary_key=True)
    title = Column(String(20, 'utf8mb4_general_ci'), nullable=False)
    description = Column(String(500, 'utf8mb4_general_ci'), nullable=False)
    photo = Column(String(255, 'utf8mb4_general_ci'))
    location_id = Column(ForeignKey('locations.location_id', ondelete='CASCADE'), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    person_performing = Column(String(20, 'utf8mb4_general_ci'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    specialty = Column(ENUM('swimming', 'fitness'), nullable=False)
    booking_deadline = Column(DateTime, nullable=False)
    organizer_id = Column(ForeignKey('event_organizer.organizer_id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    location = relationship('Location')
    organizer = relationship('EventOrganizer')


class FamilyMember(Base):
    __tablename__ = 'family_members'

    member_id = Column(Integer, primary_key=True)
    family_id = Column(ForeignKey('family_groups.family_id', ondelete='CASCADE'), nullable=False, index=True)
    full_name = Column(String(100, 'utf8mb4_general_ci'), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(ENUM('male', 'female', 'other'), nullable=False, index=True)
    relationship_type = Column(ENUM('son', 'daughter', 'other'), nullable=False, index=True, server_default=text("'other'"))
    email = Column(String(100, 'utf8mb4_general_ci'))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    family_group = relationship('FamilyGroup', back_populates='members')

class Listing(Base):
    __tablename__ = 'listing'
    __table_args__ = (
        CheckConstraint('(`current_students` >= 0)'),
        CheckConstraint('(`group_duration` > 0)'),
        CheckConstraint('(`group_price` >= 0)'),
        CheckConstraint('(`individual_duration` > 0)'),
        CheckConstraint('(`individual_price` >= 0)'),
        CheckConstraint('(`min_students` >= 0)'),
        CheckConstraint('(`sessions_per_week` > 0)'),
        Index('idx_prices', 'individual_price', 'group_price'),
        Index('idx_schedule_sessions', 'schedule_type', 'sessions_per_week'),
        Index('idx_coach_status', 'coach_id', 'status'),
        Index('idx_main_filter', 'type', 'status', 'age_group', 'skill_level')
    )

    listing_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    coach_id = Column(ForeignKey('coach.coach_id', ondelete='CASCADE'), nullable=False)
    type = Column(Enum('swimming', 'fitness'), nullable=False)
    description = Column(Text)
    session_type = Column(Enum('individual', 'group'), nullable=False)
    status = Column(Enum('active', 'inactive', 'suspended'), nullable=False, server_default=text("'active'"))
    schedule_type = Column(Enum('one-time', 'weekly', 'monthly'), nullable=False, server_default=text("'one-time'"))
    sessions_per_week = Column(Integer)
    custom_schedule = Column(JSON)
    individual_price = Column(Integer, server_default=text("'0'"))
    individual_duration = Column(Integer, server_default=text("'60'"))
    group_price = Column(Integer, server_default=text("'0'"))
    group_duration = Column(Integer, server_default=text("'60'"))
    min_students = Column(Integer, server_default=text("'0'"))
    max_students = Column(Integer, server_default=text("'10'"))
    current_students = Column(Integer, server_default=text("'0'"))
    age_group = Column(String(50), nullable=False)
    skill_level = Column(Enum('Beginner', 'Intermediate', 'Advanced'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    location_id = Column(Integer, nullable=False)

    coach = relationship('Coach')


class MarketingServicesPurchase(Base):
    __tablename__ = 'marketing_services_purchases'
    __table_args__ = (
        Index('idx_user_service', 'user_id', 'mst_id'),
        Index('idx_schedule', 'start_date', 'end_date')
    )

    msp_id = Column(Integer, primary_key=True)
    mst_id = Column(ForeignKey('marketing_services.mst_id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    content_url = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum('pending', 'approved', 'rejected', 'completed', 'cancelled', 'expired'), nullable=False, index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    posted_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    mst = relationship('MarketingService')
    user = relationship('User')


class MarketplaceFavorite(Base):
    __tablename__ = 'marketplace_favorites'
    __table_args__ = (
        Index('idx_user_listing', 'user_id', 'listing_id', unique=True),
        Index('idx_user_listing_combination', 'user_id', 'listing_id')
    )

    favorite_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    listing_id = Column(ForeignKey('marketplace_listings.listing_id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    listing = relationship('MarketplaceListing')
    user = relationship('User')


class MarketplaceMessage(Base):
    __tablename__ = 'marketplace_messages'
    __table_args__ = (
        Index('idx_sender_receiver', 'sender_id', 'receiver_id'),
    )

    message_id = Column(Integer, primary_key=True)
    sender_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    receiver_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    listing_id = Column(ForeignKey('marketplace_listings.listing_id', ondelete='CASCADE'), nullable=False, index=True)
    content = Column(Text(collation='utf8mb4_general_ci'), nullable=False)
    sent_at = Column(TIMESTAMP, index=True, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(ENUM('sent', 'read'), index=True, server_default=text("'sent'"))

    listing = relationship('MarketplaceListing')
    receiver = relationship('User', primaryjoin='MarketplaceMessage.receiver_id == User.user_id')
    sender = relationship('User', primaryjoin='MarketplaceMessage.sender_id == User.user_id')


class MarketplacePurchase(Base):
    __tablename__ = 'marketplace_purchases'
    __table_args__ = (
        CheckConstraint('(`purchase_price` >= 0)'),
    )

    purchase_id = Column(Integer, primary_key=True)
    listing_id = Column(ForeignKey('marketplace_listings.listing_id', ondelete='CASCADE'), nullable=False, index=True)
    buyer_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    seller_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    purchase_price = Column(DECIMAL(10, 2), nullable=False)
    payment_status = Column(ENUM('pending', 'completed', 'failed'), nullable=False, index=True, server_default=text("'pending'"))
    shipping_status = Column(ENUM('pending', 'shipped', 'delivered', 'cancelled', 'returned'), index=True, server_default=text("'pending'"))
    payment_method = Column(String(50, 'utf8mb4_general_ci'), index=True)
    purchase_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    buyer = relationship('User', primaryjoin='MarketplacePurchase.buyer_id == User.user_id')
    listing = relationship('MarketplaceListing')
    seller = relationship('User', primaryjoin='MarketplacePurchase.seller_id == User.user_id')


class SupportTicket(Base):
    __tablename__ = 'support_ticket'
    __table_args__ = (
        Index('idx_status_priority', 'status', 'priority'),
    )

    ticket_id = Column(Integer, primary_key=True)
    agent_id = Column(ForeignKey('support_agent.agent_id', ondelete='SET NULL'), index=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(String(100, 'utf8mb4_general_ci'), nullable=False)
    description = Column(String(1000, 'utf8mb4_general_ci'), nullable=False)
    status = Column(ENUM('open', 'in_progress', 'closed'), server_default=text("'open'"))
    priority = Column(ENUM('low', 'medium', 'high'), server_default=text("'medium'"))
    created_at = Column(TIMESTAMP, index=True, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    agent = relationship('SupportAgent')
    user = relationship('User')


class EventAttendance(Base):
    __tablename__ = 'event_attendance'
    __table_args__ = (
        Index('idx_event_attendee', 'event_id', 'attendee_id'),
    )

    attendance_id = Column(Integer, primary_key=True)
    event_id = Column(ForeignKey('event.event_id', ondelete='CASCADE'), nullable=False)
    attendee_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    status = Column(ENUM('attended', 'no-show', 'cancelled'), index=True, server_default=text("'attended'"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    attendee = relationship('User')
    event = relationship('Event')


class SessionBooking(Base):
    __tablename__ = 'session_bookings'
    __table_args__ = (
        CheckConstraint('(`booking_price` >= 0)'),
    )

    booking_id = Column(Integer, primary_key=True)
    session_id = Column(ForeignKey('marketplace_listings.listing_id', ondelete='CASCADE'), nullable=False, index=True)
    buyer_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    member_id = Column(ForeignKey('family_members.member_id', ondelete='CASCADE'), index=True)
    provider_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    provider_type = Column(ENUM('coach', 'academy'), nullable=False)
    session_type = Column(ENUM('fitness', 'swimming'), nullable=False, index=True)
    booking_price = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(ENUM('credit_card', 'paypal', 'wallet', 'cash'), nullable=False)
    payment_status = Column(ENUM('pending', 'completed', 'failed'), nullable=False, server_default=text("'pending'"))
    session_status = Column(ENUM('upcoming', 'completed', 'cancelled'), server_default=text("'upcoming'"))
    booking_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    session_date = Column(DateTime, nullable=False, index=True)
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    buyer = relationship('User', primaryjoin='SessionBooking.buyer_id == User.user_id')
    member = relationship('FamilyMember')
    provider = relationship('User', primaryjoin='SessionBooking.provider_id == User.user_id')
    session = relationship('MarketplaceListing')


class BookingTransaction(Base):
    __tablename__ = 'booking_transactions'
    __table_args__ = (
        CheckConstraint('(`amount` >= 0)'),
        CheckConstraint('(`amount` >= 0)'),
        Index('idx_booking_user', 'booking_id', 'user_id')
    )

    transaction_id = Column(Integer, primary_key=True)
    booking_id = Column(ForeignKey('session_bookings.booking_id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    recipient_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    recipient_type = Column(ENUM('coach', 'academy'), nullable=False)
    speciality = Column(ENUM('swimming', 'fitness'), nullable=False, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(ENUM('credit_card', 'paypal', 'wallet', 'bank_transfer', 'cash'), nullable=False)
    transaction_status = Column(ENUM('pending', 'successful', 'failed', 'refunded'), nullable=False, index=True, server_default=text("'pending'"))
    transaction_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    description = Column(String(255, 'utf8mb4_general_ci'), server_default=text("'No description provided'"), comment='Optional description or notes for the transaction')

    booking = relationship('SessionBooking')
    recipient = relationship('User', primaryjoin='BookingTransaction.recipient_id == User.user_id')
    user = relationship('User', primaryjoin='BookingTransaction.user_id == User.user_id')


class ChatRoom(Base):
    __tablename__ = 'chat_rooms'

    chat_room_id = Column(Integer, primary_key=True)
    session_id = Column(ForeignKey('session_bookings.session_id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = Column(TIMESTAMP, index=True, server_default=text("CURRENT_TIMESTAMP"))
    chat_room_type = Column(ENUM('individual', 'group'), nullable=False, server_default=text("'group'"), comment='Type of chat room: individual or group')

    session = relationship('SessionBooking')


class ProviderFeedback(Base):
    __tablename__ = 'provider_feedback'
    __table_args__ = (
        CheckConstraint('(`rating` between 1 and 5)'),
    )

    feedback_id = Column(Integer, primary_key=True)
    provider_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    provider_type = Column(ENUM('coach', 'academy'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    session_id = Column(ForeignKey('session_bookings.booking_id', ondelete='CASCADE'), nullable=False, index=True)
    rating = Column(TINYINT, nullable=False)
    feedback_text = Column(Text(collation='utf8mb4_general_ci'))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    provider = relationship('User', primaryjoin='ProviderFeedback.provider_id == User.user_id')
    session = relationship('SessionBooking')
    user = relationship('User', primaryjoin='ProviderFeedback.user_id == User.user_id')


class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    message_id = Column(Integer, primary_key=True)
    chat_room_id = Column(ForeignKey('chat_rooms.chat_room_id', ondelete='CASCADE'), nullable=False, index=True)
    sender_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    message_text = Column(Text, comment='Content of the message (limited to optimize storage)')
    sent_at = Column(TIMESTAMP, index=True, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(Enum('sent', 'delivered', 'read'), nullable=False, server_default=text("'sent'"), comment='Status of the message')
    message_type = Column(Enum('text', 'image', 'video', 'other'), nullable=False, server_default=text("'text'"), comment='Type of the message')

    chat_room = relationship('ChatRoom')
    sender = relationship('User')


class ChatParticipant(Base):
    __tablename__ = 'chat_participants'

    participant_id = Column(Integer, primary_key=True)
    chat_room_id = Column(ForeignKey('chat_rooms.chat_room_id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, index=True)
    role = Column(Enum('parent', 'swimmer', 'coach', 'academy'), nullable=False, index=True)
    added_at = Column(TIMESTAMP, index=True, server_default=text("CURRENT_TIMESTAMP"))
    participant_status = Column(Enum('active', 'removed'), nullable=False, server_default=text("'active'"), comment='Status of the participant in the chat room')

    chat_room = relationship('ChatRoom')
    user = relationship('User')


class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_type = Column(Enum('training_booking', 'event_booking', 'marketplace_purchase', name='transaction_type'), nullable=False)
    status = Column(Enum('pending', 'completed', 'failed', 'refunded', name='transaction_status'), default='pending')
    reference_id = Column(Integer, nullable=False)
    payment_method = Column(String(50))
    commission_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="transactions")
    refunds = relationship("Refund", back_populates="transaction")


class Refund(Base):
    __tablename__ = "refunds"
    
    refund_id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.transaction_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    reason = Column(Text, nullable=False)
    refund_type = Column(Enum('training', 'event', 'marketplace', name='refund_type'), nullable=False)
    status = Column(Enum('pending', 'approved', 'rejected', 'completed', name='refund_status'), default='pending')
    approved_by = Column(Integer, ForeignKey("user.user_id"))
    admin_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

    # Relationships
    transaction = relationship("Transaction", back_populates="refunds")
    user = relationship("User", foreign_keys=[user_id], back_populates="refunds")
    approver = relationship("User", foreign_keys=[approved_by])