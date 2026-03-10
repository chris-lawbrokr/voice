from app.models import Base
from typing import Optional
import datetime
import decimal
import uuid

from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Double, ForeignKeyConstraint, Index, Integer, JSON, Numeric, PrimaryKeyConstraint, String, Table, Text, Uuid, text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

class AbuseIpChecks(Base):
    __tablename__ = 'abuse_ip_checks'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='abuse_ip_checks_pkey'),
        Index('index_abuse_ip_checks_on_expires_at', 'expires_at'),
        Index('index_abuse_ip_checks_on_ip_address', 'ip_address', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ip_address: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    is_whitelisted: Mapped[Optional[bool]] = mapped_column(Boolean)
    abuse_confidence_score: Mapped[Optional[int]] = mapped_column(Integer)
    country_code: Mapped[Optional[str]] = mapped_column(String)
    usage_type: Mapped[Optional[str]] = mapped_column(String)
    isp: Mapped[Optional[str]] = mapped_column(String)
    domain: Mapped[Optional[str]] = mapped_column(String)
    is_tor: Mapped[Optional[bool]] = mapped_column(Boolean)
    bot_score: Mapped[Optional[int]] = mapped_column(Integer)
    checked_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    last_error: Mapped[Optional[str]] = mapped_column(Text)
    failed_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))


class ActionTextRichTexts(Base):
    __tablename__ = 'action_text_rich_texts'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='action_text_rich_texts_pkey'),
        Index('index_action_text_rich_texts_uniqueness', 'record_type', 'record_id', 'name', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    record_type: Mapped[str] = mapped_column(String, nullable=False)
    record_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    body: Mapped[Optional[str]] = mapped_column(Text)


class ActiveStorageBlobs(Base):
    __tablename__ = 'active_storage_blobs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='active_storage_blobs_pkey'),
        Index('index_active_storage_blobs_on_key', 'key', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    key: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    service_name: Mapped[str] = mapped_column(String, nullable=False)
    byte_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    content_type: Mapped[Optional[str]] = mapped_column(String)
    metadata_: Mapped[Optional[str]] = mapped_column('metadata', Text)
    checksum: Mapped[Optional[str]] = mapped_column(String)

    active_storage_attachments: Mapped[list['ActiveStorageAttachments']] = relationship('ActiveStorageAttachments', back_populates='blob')
    active_storage_variant_records: Mapped[list['ActiveStorageVariantRecords']] = relationship('ActiveStorageVariantRecords', back_populates='blob')


t_ad_home_recent_campaigns = Table(
    'ad_home_recent_campaigns', Base.metadata,
    Column('law_firm', String),
    Column('ad_campaign', String),
    Column('daily_budget', Numeric),
    Column('created', Date),
    Column('status', String)
)


t_ad_home_top_campaigns = Table(
    'ad_home_top_campaigns', Base.metadata,
    Column('theme', Text),
    Column('impressions', BigInteger),
    Column('clicks', BigInteger),
    Column('conversions', BigInteger),
    Column('ad_spend', BigInteger)
)


class AhoyEvents(Base):
    __tablename__ = 'ahoy_events'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='ahoy_events_pkey'),
        Index('index_ahoy_events_on_name_and_time', 'name', 'time'),
        Index('index_ahoy_events_on_properties', 'properties', postgresql_ops={'properties': 'jsonb_path_ops'}, postgresql_using='gin'),
        Index('index_ahoy_events_on_user_id', 'user_id'),
        Index('index_ahoy_events_on_visit_id', 'visit_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    visit_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    name: Mapped[Optional[str]] = mapped_column(String)
    properties: Mapped[Optional[dict]] = mapped_column(JSONB)
    time: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))


class AhoyVisits(Base):
    __tablename__ = 'ahoy_visits'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='ahoy_visits_pkey'),
        Index('index_ahoy_visits_on_engaged_clip_not_null', 'engaged_clip', postgresql_where='(engaged_clip IS NOT NULL)'),
        Index('index_ahoy_visits_on_user_id', 'user_id'),
        Index('index_ahoy_visits_on_visit_token', 'visit_token', unique=True),
        Index('index_ahoy_visits_on_visitor_token_and_started_at', 'visitor_token', 'started_at')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    visit_token: Mapped[Optional[str]] = mapped_column(String)
    visitor_token: Mapped[Optional[str]] = mapped_column(String)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    ip: Mapped[Optional[str]] = mapped_column(String)
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    referrer: Mapped[Optional[str]] = mapped_column(Text)
    referring_domain: Mapped[Optional[str]] = mapped_column(String)
    landing_page: Mapped[Optional[str]] = mapped_column(Text)
    browser: Mapped[Optional[str]] = mapped_column(String)
    os: Mapped[Optional[str]] = mapped_column(String)
    device_type: Mapped[Optional[str]] = mapped_column(String)
    country: Mapped[Optional[str]] = mapped_column(String)
    region: Mapped[Optional[str]] = mapped_column(String)
    city: Mapped[Optional[str]] = mapped_column(String)
    latitude: Mapped[Optional[float]] = mapped_column(Double(53))
    longitude: Mapped[Optional[float]] = mapped_column(Double(53))
    utm_source: Mapped[Optional[str]] = mapped_column(String)
    utm_medium: Mapped[Optional[str]] = mapped_column(String)
    utm_term: Mapped[Optional[str]] = mapped_column(String)
    utm_content: Mapped[Optional[str]] = mapped_column(String)
    utm_campaign: Mapped[Optional[str]] = mapped_column(String)
    app_version: Mapped[Optional[str]] = mapped_column(String)
    os_version: Mapped[Optional[str]] = mapped_column(String)
    platform: Mapped[Optional[str]] = mapped_column(String)
    started_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    raw_headers: Mapped[Optional[dict]] = mapped_column(JSONB)
    origin_url: Mapped[Optional[str]] = mapped_column(Text)
    landed_url: Mapped[Optional[str]] = mapped_column(Text)
    engaged_url: Mapped[Optional[str]] = mapped_column(Text)
    engaged_clip: Mapped[Optional[str]] = mapped_column(String)


t_analytics_average_conversion_rate_graph = Table(
    'analytics_average_conversion_rate_graph', Base.metadata,
    Column('date_month', Date),
    Column('conversion_rate', Numeric)
)


t_analytics_bottom_accounts = Table(
    'analytics_bottom_accounts', Base.metadata,
    Column('law_firm_name', String),
    Column('page_views', BigInteger),
    Column('conversions', BigInteger),
    Column('conversion_rate', Numeric)
)


t_analytics_practice_area = Table(
    'analytics_practice_area', Base.metadata,
    Column('practice_area', Text),
    Column('page_views', BigInteger),
    Column('conversions', BigInteger),
    Column('conversion_rate', Numeric)
)


t_analytics_top_accounts = Table(
    'analytics_top_accounts', Base.metadata,
    Column('law_firm_name', String),
    Column('page_views', BigInteger),
    Column('conversions', BigInteger),
    Column('conversion_rate', Numeric)
)


t_analytics_visit_conversion_graph = Table(
    'analytics_visit_conversion_graph', Base.metadata,
    Column('date_month', Date),
    Column('total_visits', BigInteger),
    Column('total_conversions', BigInteger)
)


class ArInternalMetadata(Base):
    __tablename__ = 'ar_internal_metadata'
    __table_args__ = (
        PrimaryKeyConstraint('key', name='ar_internal_metadata_pkey'),
    )

    key: Mapped[str] = mapped_column(String, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    value: Mapped[Optional[str]] = mapped_column(String)


t_home_account_activations_per_month = Table(
    'home_account_activations_per_month', Base.metadata,
    Column('date_month', DateTime),
    Column('num_activations', BigInteger)
)


t_home_recent_account_activations = Table(
    'home_recent_account_activations', Base.metadata,
    Column('law_firm_id', BigInteger),
    Column('name', String),
    Column('size', Integer),
    Column('location', String),
    Column('activation_date', Date)
)


t_justice_funnels = Table(
    'justice_funnels', Base.metadata,
    Column('law_firm_id', BigInteger),
    Column('funnel_id', BigInteger),
    Column('funnel', String),
    Column('published', Boolean)
)


t_justice_law_firms = Table(
    'justice_law_firms', Base.metadata,
    Column('law_firm_id', BigInteger),
    Column('name', String),
    Column('location', String),
    Column('website_url', String),
    Column('practice_area', Text)
)


t_justice_users = Table(
    'justice_users', Base.metadata,
    Column('law_firm_id', BigInteger),
    Column('user_id', BigInteger),
    Column('first_name', String),
    Column('last_name', String),
    Column('email', String),
    Column('company', String),
    Column('position', String),
    Column('access_token', Uuid)
)


t_justice_workflows = Table(
    'justice_workflows', Base.metadata,
    Column('law_firm_id', BigInteger),
    Column('funnel_id', BigInteger),
    Column('workflow_id', BigInteger),
    Column('workflow', String),
    Column('published', Boolean)
)


class LawFirms(Base):
    __tablename__ = 'law_firms'
    __table_args__ = (
        ForeignKeyConstraint(['primary_user_id'], ['users.id'], name='fk_rails_2079de7c77'),
        PrimaryKeyConstraint('id', name='law_firms_pkey'),
        Index('index_law_firms_on_primary_user_id', 'primary_user_id'),
        Index('index_law_firms_on_slug', 'slug', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    justice_support: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    name: Mapped[Optional[str]] = mapped_column(String)
    web: Mapped[Optional[str]] = mapped_column(String)
    bar_number: Mapped[Optional[str]] = mapped_column(String)
    employees: Mapped[Optional[str]] = mapped_column(String)
    primary_user_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    analytics: Mapped[Optional[bool]] = mapped_column(Boolean)
    integrations: Mapped[Optional[bool]] = mapped_column(Boolean)
    slug: Mapped[Optional[str]] = mapped_column(String)
    tos_url: Mapped[Optional[str]] = mapped_column(String)
    setup_step: Mapped[Optional[int]] = mapped_column(Integer)
    stripe_price_id: Mapped[Optional[str]] = mapped_column(String)
    stripe_payment_url: Mapped[Optional[str]] = mapped_column(String)
    privacy_url: Mapped[Optional[str]] = mapped_column(String)
    drips: Mapped[Optional[bool]] = mapped_column(Boolean)
    location: Mapped[Optional[str]] = mapped_column(String)
    marketing_agency: Mapped[Optional[str]] = mapped_column(String)
    marketing_spend: Mapped[Optional[int]] = mapped_column(Integer)
    tech_stack: Mapped[Optional[dict]] = mapped_column(JSONB)
    firm_size: Mapped[Optional[int]] = mapped_column(Integer)
    practice_areas: Mapped[Optional[dict]] = mapped_column(JSONB)
    google_customer_id: Mapped[Optional[str]] = mapped_column(String)
    accept_ads_tos: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    request_ads: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    enterprise: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    clips_support: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    inactive: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    request_clips: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    primary_user: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[primary_user_id], back_populates='law_firms_primary_user')
    users_law_firm: Mapped[list['Users']] = relationship('Users', foreign_keys='[Users.law_firm_id]', back_populates='law_firm')
    ad_campaigns: Mapped[list['AdCampaigns']] = relationship('AdCampaigns', back_populates='law_firm')
    api_keys: Mapped[list['ApiKeys']] = relationship('ApiKeys', back_populates='law_firm')
    automations: Mapped[list['Automations']] = relationship('Automations', back_populates='law_firm')
    images: Mapped[list['Images']] = relationship('Images', back_populates='law_firm')
    settings_integrations: Mapped[list['SettingsIntegrations']] = relationship('SettingsIntegrations', back_populates='law_firm')
    subscriptions: Mapped[list['Subscriptions']] = relationship('Subscriptions', back_populates='law_firm')
    clips: Mapped[list['Clips']] = relationship('Clips', back_populates='law_firm')
    campaigns: Mapped[list['Campaigns']] = relationship('Campaigns', back_populates='law_firm')
    landing_pages: Mapped[list['LandingPages']] = relationship('LandingPages', back_populates='law_firm')
    library_pages: Mapped[list['LibraryPages']] = relationship('LibraryPages', back_populates='law_firm')
    storefront_designs: Mapped[list['StorefrontDesigns']] = relationship('StorefrontDesigns', back_populates='law_firm')
    lead_rules: Mapped[list['LeadRules']] = relationship('LeadRules', back_populates='law_firm')
    leads: Mapped[list['Leads']] = relationship('Leads', back_populates='law_firm')


t_rewind_2025_avg_workflow_time = Table(
    'rewind_2025_avg_workflow_time', Base.metadata,
    Column('avg_completion_minutes', Integer),
    Column('avg_completion_seconds', Integer)
)


t_rewind_2025_general_analytics = Table(
    'rewind_2025_general_analytics', Base.metadata,
    Column('total_visits', BigInteger),
    Column('total_conversions', BigInteger),
    Column('avg_conversion_rate', Numeric)
)


t_rewind_2025_mobile_traffic = Table(
    'rewind_2025_mobile_traffic', Base.metadata,
    Column('device_type', Text),
    Column('visit_count', BigInteger),
    Column('percent', Numeric)
)


t_rewind_2025_top_law_firms = Table(
    'rewind_2025_top_law_firms', Base.metadata,
    Column('law_firm_name', String),
    Column('total_leads', BigInteger),
    Column('total_conversions', BigInteger),
    Column('conversion_rate', Numeric)
)


t_rewind_2025_top_locations = Table(
    'rewind_2025_top_locations', Base.metadata,
    Column('state', String),
    Column('visit_count', BigInteger),
    Column('percent', Numeric)
)


t_rewind_2025_top_practice_areas = Table(
    'rewind_2025_top_practice_areas', Base.metadata,
    Column('practice_area', Text),
    Column('total_visits', BigInteger),
    Column('total_conversions', BigInteger),
    Column('avg_conversion_rate', Numeric)
)


class SchemaMigrations(Base):
    __tablename__ = 'schema_migrations'
    __table_args__ = (
        PrimaryKeyConstraint('version', name='schema_migrations_pkey'),
    )

    version: Mapped[str] = mapped_column(String, primary_key=True)


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_3b40951616'),
        PrimaryKeyConstraint('id', name='users_pkey'),
        Index('index_users_on_access_token', 'access_token', unique=True),
        Index('index_users_on_email', 'email'),
        Index('index_users_on_law_firm_id', 'law_firm_id'),
        Index('index_users_on_remember_token', 'remember_token')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    remember_token: Mapped[str] = mapped_column(String(128), nullable=False)
    access_token: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, server_default=text('gen_random_uuid()'))
    encrypted_password: Mapped[Optional[str]] = mapped_column(String(128))
    confirmation_token: Mapped[Optional[str]] = mapped_column(String(128))
    role: Mapped[Optional[int]] = mapped_column(Integer)
    first_name: Mapped[Optional[str]] = mapped_column(String)
    last_name: Mapped[Optional[str]] = mapped_column(String)
    phone: Mapped[Optional[str]] = mapped_column(String)
    email_confirmation_token: Mapped[Optional[str]] = mapped_column(String)
    email_confirmed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    law_firm_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    agree_to_terms: Mapped[Optional[bool]] = mapped_column(Boolean)
    company: Mapped[Optional[str]] = mapped_column(String)
    lead_notifications: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    integration_notifications: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    setup_step: Mapped[Optional[int]] = mapped_column(Integer)
    position: Mapped[Optional[str]] = mapped_column(String)
    platform_notifications: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    law_firms_primary_user: Mapped[list['LawFirms']] = relationship('LawFirms', foreign_keys='[LawFirms.primary_user_id]', back_populates='primary_user')
    law_firm: Mapped[Optional['LawFirms']] = relationship('LawFirms', foreign_keys=[law_firm_id], back_populates='users_law_firm')
    lead_recipients: Mapped[list['LeadRecipients']] = relationship('LeadRecipients', back_populates='user')
    lead_rules: Mapped[list['LeadRules']] = relationship('LeadRules', back_populates='user')


class Videos(Base):
    __tablename__ = 'videos'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='videos_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String)
    asset_id: Mapped[Optional[str]] = mapped_column(String)
    playback_id: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[Optional[str]] = mapped_column(String)
    law_firm_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    clips: Mapped[list['Clips']] = relationship('Clips', back_populates='video')


class ActiveStorageAttachments(Base):
    __tablename__ = 'active_storage_attachments'
    __table_args__ = (
        ForeignKeyConstraint(['blob_id'], ['active_storage_blobs.id'], name='fk_rails_c3b3935057'),
        PrimaryKeyConstraint('id', name='active_storage_attachments_pkey'),
        Index('index_active_storage_attachments_on_blob_id', 'blob_id'),
        Index('index_active_storage_attachments_uniqueness', 'record_type', 'record_id', 'name', 'blob_id', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    record_type: Mapped[str] = mapped_column(String, nullable=False)
    record_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    blob_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)

    blob: Mapped['ActiveStorageBlobs'] = relationship('ActiveStorageBlobs', back_populates='active_storage_attachments')


class ActiveStorageVariantRecords(Base):
    __tablename__ = 'active_storage_variant_records'
    __table_args__ = (
        ForeignKeyConstraint(['blob_id'], ['active_storage_blobs.id'], name='fk_rails_993965df05'),
        PrimaryKeyConstraint('id', name='active_storage_variant_records_pkey'),
        Index('index_active_storage_variant_records_uniqueness', 'blob_id', 'variation_digest', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    blob_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    variation_digest: Mapped[str] = mapped_column(String, nullable=False)

    blob: Mapped['ActiveStorageBlobs'] = relationship('ActiveStorageBlobs', back_populates='active_storage_variant_records')


class AdCampaigns(Base):
    __tablename__ = 'ad_campaigns'
    __table_args__ = (
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_0ae1855450'),
        PrimaryKeyConstraint('id', name='ad_campaigns_pkey'),
        Index('index_ad_campaigns_on_identifier', 'identifier', unique=True),
        Index('index_ad_campaigns_on_law_firm_id', 'law_firm_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    law_firm_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String)
    identifier: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[Optional[str]] = mapped_column(String)
    locations: Mapped[Optional[dict]] = mapped_column(JSONB)
    language: Mapped[Optional[str]] = mapped_column(String)
    themes: Mapped[Optional[dict]] = mapped_column(JSONB)
    negative_themes: Mapped[Optional[dict]] = mapped_column(JSONB)
    budget_micros: Mapped[Optional[int]] = mapped_column(BigInteger)
    google_campaign_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    campaign_resource: Mapped[Optional[str]] = mapped_column(String)
    budget_resource: Mapped[Optional[str]] = mapped_column(String)
    ad_group_resource: Mapped[Optional[str]] = mapped_column(String)
    ad_resource: Mapped[Optional[str]] = mapped_column(String)
    serving_status: Mapped[Optional[str]] = mapped_column(String)

    law_firm: Mapped['LawFirms'] = relationship('LawFirms', back_populates='ad_campaigns')
    ad_events: Mapped[list['AdEvents']] = relationship('AdEvents', back_populates='ad_campaign')
    ad_metrics: Mapped[list['AdMetrics']] = relationship('AdMetrics', back_populates='ad_campaign')
    ad_reviews: Mapped[list['AdReviews']] = relationship('AdReviews', back_populates='ad_campaign')
    landing_pages: Mapped[list['LandingPages']] = relationship('LandingPages', back_populates='ad_campaign')


class ApiKeys(Base):
    __tablename__ = 'api_keys'
    __table_args__ = (
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_13f980b14d'),
        PrimaryKeyConstraint('id', name='api_keys_pkey'),
        Index('index_api_keys_on_law_firm_id', 'law_firm_id'),
        Index('index_api_keys_on_token', 'token', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    law_firm_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    name: Mapped[Optional[str]] = mapped_column(String)
    token: Mapped[Optional[str]] = mapped_column(String)
    scope: Mapped[Optional[str]] = mapped_column(String, server_default=text("'local'::character varying"))
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

    law_firm: Mapped[Optional['LawFirms']] = relationship('LawFirms', back_populates='api_keys')


class Automations(Base):
    __tablename__ = 'automations'
    __table_args__ = (
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_dca10757ea'),
        PrimaryKeyConstraint('id', name='automations_pkey'),
        Index('index_automations_on_law_firm_id', 'law_firm_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    law_firm_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String)
    name: Mapped[Optional[str]] = mapped_column(String)
    protocol: Mapped[Optional[str]] = mapped_column(String)
    active: Mapped[Optional[bool]] = mapped_column(Boolean)
    subject: Mapped[Optional[str]] = mapped_column(String)
    sender: Mapped[Optional[str]] = mapped_column(String)
    reply_to: Mapped[Optional[str]] = mapped_column(String)
    button_text: Mapped[Optional[str]] = mapped_column(String)
    button_url: Mapped[Optional[str]] = mapped_column(String)
    signature: Mapped[Optional[str]] = mapped_column(String)
    content: Mapped[Optional[str]] = mapped_column(Text)
    delay_send: Mapped[Optional[int]] = mapped_column(Integer)
    color: Mapped[Optional[str]] = mapped_column(String)
    show_logo: Mapped[Optional[bool]] = mapped_column(Boolean)
    trigger: Mapped[Optional[str]] = mapped_column(String)

    law_firm: Mapped['LawFirms'] = relationship('LawFirms', back_populates='automations')
    automation_journeys: Mapped[list['AutomationJourneys']] = relationship('AutomationJourneys', back_populates='automation')
    automation_events: Mapped[list['AutomationEvents']] = relationship('AutomationEvents', back_populates='automation')


class Images(Base):
    __tablename__ = 'images'
    __table_args__ = (
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_d1cda3c638'),
        PrimaryKeyConstraint('id', name='images_pkey'),
        Index('index_images_on_law_firm_id', 'law_firm_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    law_firm_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    image_type: Mapped[str] = mapped_column(String, nullable=False)
    image_name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String)
    deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    metadata_: Mapped[Optional[dict]] = mapped_column('metadata', JSON, server_default=text("'{}'::json"))

    law_firm: Mapped['LawFirms'] = relationship('LawFirms', back_populates='images')
    clips: Mapped[list['Clips']] = relationship('Clips', back_populates='image')
    campaigns: Mapped[list['Campaigns']] = relationship('Campaigns', back_populates='image')
    storefront_designs: Mapped[list['StorefrontDesigns']] = relationship('StorefrontDesigns', back_populates='image')
    landing_page_sections: Mapped[list['LandingPageSections']] = relationship('LandingPageSections', back_populates='image')


class SettingsIntegrations(Base):
    __tablename__ = 'settings_integrations'
    __table_args__ = (
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_22f96217bd'),
        PrimaryKeyConstraint('id', name='settings_integrations_pkey'),
        Index('index_settings_integrations_on_law_firm_id', 'law_firm_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    law_firm_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String)
    type: Mapped[Optional[str]] = mapped_column(String)

    law_firm: Mapped['LawFirms'] = relationship('LawFirms', back_populates='settings_integrations')
    settings_integration_values: Mapped[list['SettingsIntegrationValues']] = relationship('SettingsIntegrationValues', back_populates='settings_integration')
    settings_lead_integration_statuses: Mapped[list['SettingsLeadIntegrationStatuses']] = relationship('SettingsLeadIntegrationStatuses', back_populates='settings_integration')


class Subscriptions(Base):
    __tablename__ = 'subscriptions'
    __table_args__ = (
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_cc0345cde8'),
        PrimaryKeyConstraint('id', name='subscriptions_pkey'),
        Index('index_subscriptions_on_law_firm_id', 'law_firm_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    law_firm_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String)
    last_paid_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    period: Mapped[Optional[str]] = mapped_column(String)
    next_payment_due_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    payment_paused: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    law_firm: Mapped['LawFirms'] = relationship('LawFirms', back_populates='subscriptions')


class AdEvents(Base):
    __tablename__ = 'ad_events'
    __table_args__ = (
        ForeignKeyConstraint(['ad_campaign_id'], ['ad_campaigns.id'], name='fk_rails_f34e21c80c'),
        PrimaryKeyConstraint('id', name='ad_events_pkey'),
        Index('index_ad_events_on_ad_campaign_id', 'ad_campaign_id'),
        Index('index_ad_events_on_ad_campaign_id_and_event', 'ad_campaign_id', 'event')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ad_campaign_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    event: Mapped[Optional[str]] = mapped_column(String)
    keywords: Mapped[Optional[dict]] = mapped_column(JSONB)
    negative_keywords: Mapped[Optional[dict]] = mapped_column(JSONB)
    ads: Mapped[Optional[dict]] = mapped_column(JSONB)

    ad_campaign: Mapped['AdCampaigns'] = relationship('AdCampaigns', back_populates='ad_events')


class AdMetrics(Base):
    __tablename__ = 'ad_metrics'
    __table_args__ = (
        ForeignKeyConstraint(['ad_campaign_id'], ['ad_campaigns.id'], name='fk_rails_7f8fd4eabf'),
        PrimaryKeyConstraint('id', name='ad_metrics_pkey'),
        Index('index_ad_metrics_on_ad_campaign_id', 'ad_campaign_id'),
        Index('index_ad_metrics_on_metric_and_period', 'metric', 'period')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ad_campaign_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    metric: Mapped[Optional[str]] = mapped_column(String)
    period: Mapped[Optional[str]] = mapped_column(String)
    device: Mapped[Optional[str]] = mapped_column(String)
    impressions: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    clicks: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    ctr: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    conversions: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    average_cpc: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    cost_per_conversion: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    cost_micros: Mapped[Optional[int]] = mapped_column(BigInteger)

    ad_campaign: Mapped['AdCampaigns'] = relationship('AdCampaigns', back_populates='ad_metrics')


class AdReviews(Base):
    __tablename__ = 'ad_reviews'
    __table_args__ = (
        ForeignKeyConstraint(['ad_campaign_id'], ['ad_campaigns.id'], name='fk_rails_59abbf5712'),
        PrimaryKeyConstraint('id', name='ad_reviews_pkey'),
        Index('index_ad_reviews_on_ad_campaign_id', 'ad_campaign_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ad_campaign_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    google_analytics: Mapped[Optional[str]] = mapped_column(Text)
    key_metrics: Mapped[Optional[str]] = mapped_column(Text)
    keywords: Mapped[Optional[str]] = mapped_column(Text)
    search_terms: Mapped[Optional[str]] = mapped_column(Text)
    ad_quality: Mapped[Optional[str]] = mapped_column(Text)
    update_keywords: Mapped[Optional[str]] = mapped_column(Text)
    update_ad: Mapped[Optional[str]] = mapped_column(Text)
    additional_notes: Mapped[Optional[str]] = mapped_column(Text)

    ad_campaign: Mapped['AdCampaigns'] = relationship('AdCampaigns', back_populates='ad_reviews')


class Clips(Base):
    __tablename__ = 'clips'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], name='fk_rails_bd8da3d3b0'),
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_8e0a13b2f8'),
        ForeignKeyConstraint(['video_id'], ['videos.id'], name='fk_rails_b8e2fc769f'),
        PrimaryKeyConstraint('id', name='clips_pkey'),
        Index('index_clips_on_image_id', 'image_id'),
        Index('index_clips_on_law_firm_id', 'law_firm_id'),
        Index('index_clips_on_token', 'token', unique=True),
        Index('index_clips_on_video_id', 'video_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    law_firm_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    video_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    image_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    name: Mapped[Optional[str]] = mapped_column(String)
    token: Mapped[Optional[str]] = mapped_column(String)
    button_text: Mapped[Optional[str]] = mapped_column(String)
    destination_url: Mapped[Optional[str]] = mapped_column(Text)
    show_button: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    button_font: Mapped[Optional[str]] = mapped_column(String)
    button_color: Mapped[Optional[str]] = mapped_column(String)
    button_text_color: Mapped[Optional[str]] = mapped_column(String)
    button_shape: Mapped[Optional[str]] = mapped_column(String)
    color: Mapped[Optional[str]] = mapped_column(String)
    align_right: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    preview: Mapped[Optional[bool]] = mapped_column(Boolean)
    custom_url: Mapped[Optional[str]] = mapped_column(Text)

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='clips')
    law_firm: Mapped['LawFirms'] = relationship('LawFirms', back_populates='clips')
    video: Mapped[Optional['Videos']] = relationship('Videos', back_populates='clips')
    campaigns: Mapped[list['Campaigns']] = relationship('Campaigns', back_populates='clip')
    landing_pages: Mapped[list['LandingPages']] = relationship('LandingPages', back_populates='clip')
    library_pages: Mapped[list['LibraryPages']] = relationship('LibraryPages', back_populates='clip')
    storefront_designs: Mapped[list['StorefrontDesigns']] = relationship('StorefrontDesigns', back_populates='clip')
    pages: Mapped[list['Pages']] = relationship('Pages', back_populates='clip')


class SettingsIntegrationValues(Base):
    __tablename__ = 'settings_integration_values'
    __table_args__ = (
        ForeignKeyConstraint(['settings_integration_id'], ['settings_integrations.id'], name='fk_rails_2ad39f59a7'),
        PrimaryKeyConstraint('id', name='settings_integration_values_pkey'),
        Index('index_settings_integration_values_on_settings_integration_id', 'settings_integration_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    settings_integration_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String)
    value: Mapped[Optional[str]] = mapped_column(String)

    settings_integration: Mapped['SettingsIntegrations'] = relationship('SettingsIntegrations', back_populates='settings_integration_values')


class Campaigns(Base):
    __tablename__ = 'campaigns'
    __table_args__ = (
        ForeignKeyConstraint(['clip_id'], ['clips.id'], name='fk_rails_c55eac8a56'),
        ForeignKeyConstraint(['image_id'], ['images.id'], name='fk_rails_e10dd9806f'),
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_d8b3786652'),
        PrimaryKeyConstraint('id', name='campaigns_pkey'),
        Index('index_campaigns_on_clip_id', 'clip_id'),
        Index('index_campaigns_on_image_id', 'image_id'),
        Index('index_campaigns_on_law_firm_id', 'law_firm_id'),
        Index('index_campaigns_on_law_firm_id_and_name', 'law_firm_id', 'name', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    law_firm_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String)
    slug: Mapped[Optional[str]] = mapped_column(String)
    color: Mapped[Optional[str]] = mapped_column(String)
    order: Mapped[Optional[int]] = mapped_column(Integer)
    published: Mapped[Optional[bool]] = mapped_column(Boolean)
    button_text: Mapped[Optional[str]] = mapped_column(String)
    heading: Mapped[Optional[str]] = mapped_column(String)
    paragraph: Mapped[Optional[str]] = mapped_column(String)
    show_logo: Mapped[Optional[bool]] = mapped_column(Boolean)
    brand_color: Mapped[Optional[str]] = mapped_column(String)
    heading_font: Mapped[Optional[str]] = mapped_column(String)
    body_font: Mapped[Optional[str]] = mapped_column(String)
    integrations_enabled: Mapped[Optional[bool]] = mapped_column(Boolean)
    color_scheme: Mapped[Optional[int]] = mapped_column(Integer)
    layout: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    theme: Mapped[Optional[str]] = mapped_column(String)
    button_shape: Mapped[Optional[str]] = mapped_column(String)
    button_style: Mapped[Optional[str]] = mapped_column(String)
    theme_image: Mapped[Optional[str]] = mapped_column(String)
    image_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    logo_url: Mapped[Optional[str]] = mapped_column(String)
    text_color: Mapped[Optional[str]] = mapped_column(String)
    attorney_share_enabled: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    clip_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    hidden: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    clip: Mapped[Optional['Clips']] = relationship('Clips', back_populates='campaigns')
    image: Mapped[Optional['Images']] = relationship('Images', back_populates='campaigns')
    law_firm: Mapped['LawFirms'] = relationship('LawFirms', back_populates='campaigns')
    journeys: Mapped[list['Journeys']] = relationship('Journeys', back_populates='campaign')
    lead_recipients: Mapped[list['LeadRecipients']] = relationship('LeadRecipients', back_populates='campaign')
    lead_rules: Mapped[list['LeadRules']] = relationship('LeadRules', back_populates='campaign')
    leads: Mapped[list['Leads']] = relationship('Leads', back_populates='campaign')


class LandingPages(Base):
    __tablename__ = 'landing_pages'
    __table_args__ = (
        ForeignKeyConstraint(['ad_campaign_id'], ['ad_campaigns.id'], name='fk_rails_8e6db0a8d2'),
        ForeignKeyConstraint(['clip_id'], ['clips.id'], name='fk_rails_82451c0cc4'),
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_8d1c06e769'),
        PrimaryKeyConstraint('id', name='landing_pages_pkey'),
        Index('index_landing_pages_on_ad_campaign_id', 'ad_campaign_id'),
        Index('index_landing_pages_on_clip_id', 'clip_id'),
        Index('index_landing_pages_on_law_firm_id', 'law_firm_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    law_firm_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    slug: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(Text)
    global_url: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    show_logo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    heading_font: Mapped[Optional[str]] = mapped_column(String)
    body_font: Mapped[Optional[str]] = mapped_column(String)
    button_shape: Mapped[Optional[str]] = mapped_column(String)
    button_style: Mapped[Optional[str]] = mapped_column(String)
    background_color: Mapped[Optional[str]] = mapped_column(String)
    text_color: Mapped[Optional[str]] = mapped_column(String)
    button_color: Mapped[Optional[str]] = mapped_column(String)
    button_text_color: Mapped[Optional[str]] = mapped_column(String)
    theme: Mapped[Optional[str]] = mapped_column(String)
    published: Mapped[Optional[bool]] = mapped_column(Boolean)
    title_tag: Mapped[Optional[str]] = mapped_column(String)
    meta_description: Mapped[Optional[str]] = mapped_column(String)
    google_analytics_id: Mapped[Optional[str]] = mapped_column(String)
    logo_id: Mapped[Optional[int]] = mapped_column(Integer)
    color: Mapped[Optional[str]] = mapped_column(String)
    google_conversion_code: Mapped[Optional[str]] = mapped_column(Text)
    goal: Mapped[Optional[int]] = mapped_column(Integer)
    ad_campaign_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    logo_url: Mapped[Optional[str]] = mapped_column(String)
    secondary_button_color: Mapped[Optional[str]] = mapped_column(String)
    secondary_button_text_color: Mapped[Optional[str]] = mapped_column(String)
    secondary_button_shape: Mapped[Optional[str]] = mapped_column(String)
    secondary_button_style: Mapped[Optional[str]] = mapped_column(String)
    clip_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    ad_campaign: Mapped[Optional['AdCampaigns']] = relationship('AdCampaigns', back_populates='landing_pages')
    clip: Mapped[Optional['Clips']] = relationship('Clips', back_populates='landing_pages')
    law_firm: Mapped['LawFirms'] = relationship('LawFirms', back_populates='landing_pages')
    landing_page_sections: Mapped[list['LandingPageSections']] = relationship('LandingPageSections', back_populates='landing_page')
    leads: Mapped[list['Leads']] = relationship('Leads', back_populates='landing_page')


class LibraryPages(Base):
    __tablename__ = 'library_pages'
    __table_args__ = (
        ForeignKeyConstraint(['clip_id'], ['clips.id'], name='fk_rails_c81256e7ac'),
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_e809df28e7'),
        PrimaryKeyConstraint('id', name='library_pages_pkey'),
        Index('index_library_pages_on_clip_id', 'clip_id'),
        Index('index_library_pages_on_law_firm_id', 'law_firm_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    law_firm_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String)
    heading: Mapped[Optional[str]] = mapped_column(String)
    subtext: Mapped[Optional[str]] = mapped_column(Text)
    required: Mapped[Optional[bool]] = mapped_column(Boolean)
    first_name: Mapped[Optional[bool]] = mapped_column(Boolean)
    last_name: Mapped[Optional[bool]] = mapped_column(Boolean)
    phone: Mapped[Optional[bool]] = mapped_column(Boolean)
    email: Mapped[Optional[bool]] = mapped_column(Boolean)
    company: Mapped[Optional[bool]] = mapped_column(Boolean)
    button_text: Mapped[Optional[str]] = mapped_column(String)
    button_url: Mapped[Optional[str]] = mapped_column(String)
    button2_text: Mapped[Optional[str]] = mapped_column(String)
    button2_url: Mapped[Optional[str]] = mapped_column(String)
    consent: Mapped[Optional[bool]] = mapped_column(Boolean)
    consent_text: Mapped[Optional[str]] = mapped_column(String)
    middle_name: Mapped[Optional[bool]] = mapped_column(Boolean)
    order: Mapped[Optional[int]] = mapped_column(Integer)
    minimum: Mapped[Optional[int]] = mapped_column(Integer)
    maximum: Mapped[Optional[int]] = mapped_column(Integer)
    consent_required: Mapped[Optional[bool]] = mapped_column(Boolean)
    privilege_required: Mapped[Optional[bool]] = mapped_column(Boolean)
    phone_required: Mapped[Optional[bool]] = mapped_column(Boolean)
    email_required: Mapped[Optional[bool]] = mapped_column(Boolean)
    custom_checkbox: Mapped[Optional[bool]] = mapped_column(Boolean)
    custom_checkbox_required: Mapped[Optional[bool]] = mapped_column(Boolean)
    custom_checkbox_message: Mapped[Optional[str]] = mapped_column(String)
    clip_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    clip: Mapped[Optional['Clips']] = relationship('Clips', back_populates='library_pages')
    law_firm: Mapped['LawFirms'] = relationship('LawFirms', back_populates='library_pages')
    library_answer_options: Mapped[list['LibraryAnswerOptions']] = relationship('LibraryAnswerOptions', back_populates='library_page')
    pages: Mapped[list['Pages']] = relationship('Pages', back_populates='source_library_page')


class StorefrontDesigns(Base):
    __tablename__ = 'storefront_designs'
    __table_args__ = (
        ForeignKeyConstraint(['clip_id'], ['clips.id'], name='fk_rails_214f90273b'),
        ForeignKeyConstraint(['image_id'], ['images.id'], name='fk_rails_e49ddc1ac6'),
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_023437d819'),
        PrimaryKeyConstraint('id', name='storefront_designs_pkey'),
        Index('index_storefront_designs_on_clip_id', 'clip_id'),
        Index('index_storefront_designs_on_image_id', 'image_id'),
        Index('index_storefront_designs_on_law_firm_id', 'law_firm_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    law_firm_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    show_journey_progress: Mapped[Optional[bool]] = mapped_column(Boolean)
    show_success_button: Mapped[Optional[bool]] = mapped_column(Boolean)
    success_button_text: Mapped[Optional[str]] = mapped_column(Text)
    success_button_url: Mapped[Optional[str]] = mapped_column(Text)
    brand_color: Mapped[Optional[str]] = mapped_column(String)
    text_color: Mapped[Optional[str]] = mapped_column(String)
    show_logo: Mapped[Optional[bool]] = mapped_column(Boolean)
    color_scheme: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    custom_code: Mapped[Optional[str]] = mapped_column(Text)
    google_tag: Mapped[Optional[str]] = mapped_column(Text)
    meta_pixel: Mapped[Optional[str]] = mapped_column(Text)
    heading: Mapped[Optional[str]] = mapped_column(String)
    paragraph: Mapped[Optional[str]] = mapped_column(String)
    heading_font: Mapped[Optional[str]] = mapped_column(String)
    body_font: Mapped[Optional[str]] = mapped_column(String)
    theme: Mapped[Optional[str]] = mapped_column(String, server_default=text("'theme 1'::character varying"))
    button_shape: Mapped[Optional[str]] = mapped_column(String, server_default=text("'pill'::character varying"))
    button_style: Mapped[Optional[str]] = mapped_column(String, server_default=text("'shadow'::character varying"))
    theme_image: Mapped[Optional[str]] = mapped_column(String)
    custom_conversion: Mapped[Optional[str]] = mapped_column(String)
    custom_error: Mapped[Optional[str]] = mapped_column(String)
    image_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    google_analytics_id: Mapped[Optional[str]] = mapped_column(String)
    google_conversion_code: Mapped[Optional[str]] = mapped_column(Text)
    logo_url: Mapped[Optional[str]] = mapped_column(String)
    clip_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    clip: Mapped[Optional['Clips']] = relationship('Clips', back_populates='storefront_designs')
    image: Mapped[Optional['Images']] = relationship('Images', back_populates='storefront_designs')
    law_firm: Mapped['LawFirms'] = relationship('LawFirms', back_populates='storefront_designs')


class Journeys(Base):
    __tablename__ = 'journeys'
    __table_args__ = (
        ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], name='fk_rails_11a33b1a13'),
        PrimaryKeyConstraint('id', name='journeys_pkey'),
        Index('index_journeys_on_campaign_id', 'campaign_id'),
        Index('index_journeys_on_campaign_id_and_name', 'campaign_id', 'name', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String)
    published: Mapped[Optional[bool]] = mapped_column(Boolean)
    slug: Mapped[Optional[str]] = mapped_column(String)
    order: Mapped[Optional[int]] = mapped_column(Integer)
    show_progress: Mapped[Optional[bool]] = mapped_column(Boolean)
    button_text: Mapped[Optional[str]] = mapped_column(String)
    color: Mapped[Optional[str]] = mapped_column(String)

    campaign: Mapped['Campaigns'] = relationship('Campaigns', back_populates='journeys')
    automation_journeys: Mapped[list['AutomationJourneys']] = relationship('AutomationJourneys', back_populates='journey')
    leads: Mapped[list['Leads']] = relationship('Leads', back_populates='journey')
    pages: Mapped[list['Pages']] = relationship('Pages', back_populates='journey')


class LandingPageSections(Base):
    __tablename__ = 'landing_page_sections'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], name='fk_rails_a0550e5a43'),
        ForeignKeyConstraint(['landing_page_id'], ['landing_pages.id'], name='fk_rails_104cd524e8'),
        PrimaryKeyConstraint('id', name='landing_page_sections_pkey'),
        Index('index_landing_page_sections_on_image_id', 'image_id'),
        Index('index_landing_page_sections_on_landing_page_id', 'landing_page_id'),
        Index('index_landing_page_sections_on_type', 'type')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    landing_page_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String)
    heading: Mapped[Optional[str]] = mapped_column(Text)
    paragraph: Mapped[Optional[str]] = mapped_column(Text)
    show_section: Mapped[Optional[bool]] = mapped_column(Boolean)
    alignment: Mapped[Optional[str]] = mapped_column(String)
    buttons: Mapped[Optional[dict]] = mapped_column(JSONB)
    content: Mapped[Optional[dict]] = mapped_column(JSONB)
    image_placement: Mapped[Optional[str]] = mapped_column(String)
    show_overlay: Mapped[Optional[bool]] = mapped_column(Boolean)
    overlay_color: Mapped[Optional[str]] = mapped_column(String)
    overlay_opacity: Mapped[Optional[float]] = mapped_column(Double(53))
    order: Mapped[Optional[int]] = mapped_column(Integer)
    image_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    show_image: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    video_link: Mapped[Optional[str]] = mapped_column(String)
    video_alignment: Mapped[Optional[str]] = mapped_column(String)
    member_configuration: Mapped[Optional[str]] = mapped_column(String)
    background_color: Mapped[Optional[str]] = mapped_column(String)
    logo_id: Mapped[Optional[int]] = mapped_column(Integer)
    logo_url: Mapped[Optional[str]] = mapped_column(String)
    show_logo: Mapped[Optional[bool]] = mapped_column(Boolean)
    text_color: Mapped[Optional[str]] = mapped_column(String)
    layout: Mapped[Optional[str]] = mapped_column(String)
    media_type: Mapped[Optional[str]] = mapped_column(String)
    image_ratio: Mapped[Optional[str]] = mapped_column(String)

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='landing_page_sections')
    landing_page: Mapped['LandingPages'] = relationship('LandingPages', back_populates='landing_page_sections')


class LeadRecipients(Base):
    __tablename__ = 'lead_recipients'
    __table_args__ = (
        ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], name='fk_rails_fbacb5f4a7'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_rails_9fe17ecc07'),
        PrimaryKeyConstraint('id', name='lead_recipients_pkey'),
        Index('index_lead_recipients_on_campaign_id', 'campaign_id'),
        Index('index_lead_recipients_on_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    campaign_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    send_lead: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    campaign: Mapped['Campaigns'] = relationship('Campaigns', back_populates='lead_recipients')
    user: Mapped['Users'] = relationship('Users', back_populates='lead_recipients')


class LeadRules(Base):
    __tablename__ = 'lead_rules'
    __table_args__ = (
        ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], name='fk_rails_2a652410ab'),
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_1ca4449021'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_rails_9447976708'),
        PrimaryKeyConstraint('id', name='lead_rules_pkey'),
        Index('index_lead_rules_on_campaign_id', 'campaign_id'),
        Index('index_lead_rules_on_law_firm_id', 'law_firm_id'),
        Index('index_lead_rules_on_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    law_firm_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    campaign_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    question: Mapped[Optional[str]] = mapped_column(Text)

    campaign: Mapped[Optional['Campaigns']] = relationship('Campaigns', back_populates='lead_rules')
    law_firm: Mapped['LawFirms'] = relationship('LawFirms', back_populates='lead_rules')
    user: Mapped['Users'] = relationship('Users', back_populates='lead_rules')


class LibraryAnswerOptions(Base):
    __tablename__ = 'library_answer_options'
    __table_args__ = (
        ForeignKeyConstraint(['library_page_id'], ['library_pages.id'], name='fk_rails_1bb9a79b20'),
        PrimaryKeyConstraint('id', name='library_answer_options_pkey'),
        Index('index_library_answer_options_on_library_page_id', 'library_page_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    library_page_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    body: Mapped[Optional[str]] = mapped_column(Text)
    order: Mapped[Optional[int]] = mapped_column(Integer)

    library_page: Mapped['LibraryPages'] = relationship('LibraryPages', back_populates='library_answer_options')


class AutomationJourneys(Base):
    __tablename__ = 'automation_journeys'
    __table_args__ = (
        ForeignKeyConstraint(['automation_id'], ['automations.id'], name='fk_rails_723487783d'),
        ForeignKeyConstraint(['journey_id'], ['journeys.id'], name='fk_rails_90da296e9f'),
        PrimaryKeyConstraint('id', name='automation_journeys_pkey'),
        Index('index_automation_journeys_on_automation_id', 'automation_id'),
        Index('index_automation_journeys_on_journey_id', 'journey_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    automation_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    journey_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)

    automation: Mapped['Automations'] = relationship('Automations', back_populates='automation_journeys')
    journey: Mapped['Journeys'] = relationship('Journeys', back_populates='automation_journeys')


class Leads(Base):
    __tablename__ = 'leads'
    __table_args__ = (
        ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], name='fk_rails_44f08376b0'),
        ForeignKeyConstraint(['journey_id'], ['journeys.id'], name='fk_rails_b6660edbe1'),
        ForeignKeyConstraint(['landing_page_id'], ['landing_pages.id'], name='fk_rails_9515df761f'),
        ForeignKeyConstraint(['law_firm_id'], ['law_firms.id'], name='fk_rails_1404dade9c'),
        PrimaryKeyConstraint('id', name='leads_pkey'),
        Index('index_leads_on_ahoy_visit_id', 'ahoy_visit_id'),
        Index('index_leads_on_campaign_id', 'campaign_id'),
        Index('index_leads_on_discarded_at', 'discarded_at'),
        Index('index_leads_on_journey_id', 'journey_id'),
        Index('index_leads_on_landing_page_id', 'landing_page_id'),
        Index('index_leads_on_law_firm_id', 'law_firm_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    email: Mapped[Optional[str]] = mapped_column(String)
    phone: Mapped[Optional[str]] = mapped_column(String)
    journey_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    first_name: Mapped[Optional[str]] = mapped_column(String)
    last_name: Mapped[Optional[str]] = mapped_column(String)
    law_firm_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    campaign_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    started: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    discarded_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    read_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    company: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(String)
    ahoy_visit_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    preview: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    started_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    resumed_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    middle_name: Mapped[Optional[str]] = mapped_column(String)
    landing_page_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    consent_opt_in: Mapped[Optional[bool]] = mapped_column(Boolean)
    secondary_consent_opt_in: Mapped[Optional[bool]] = mapped_column(Boolean)
    custom_checkbox: Mapped[Optional[bool]] = mapped_column(Boolean)
    manual_input_source: Mapped[Optional[str]] = mapped_column(Text)

    campaign: Mapped[Optional['Campaigns']] = relationship('Campaigns', back_populates='leads')
    journey: Mapped[Optional['Journeys']] = relationship('Journeys', back_populates='leads')
    landing_page: Mapped[Optional['LandingPages']] = relationship('LandingPages', back_populates='leads')
    law_firm: Mapped[Optional['LawFirms']] = relationship('LawFirms', back_populates='leads')
    automation_events: Mapped[list['AutomationEvents']] = relationship('AutomationEvents', back_populates='lead')
    responses: Mapped[list['Responses']] = relationship('Responses', back_populates='lead')
    settings_lead_integration_statuses: Mapped[list['SettingsLeadIntegrationStatuses']] = relationship('SettingsLeadIntegrationStatuses', back_populates='lead')


class Pages(Base):
    __tablename__ = 'pages'
    __table_args__ = (
        ForeignKeyConstraint(['clip_id'], ['clips.id'], name='fk_rails_6668059498'),
        ForeignKeyConstraint(['journey_id'], ['journeys.id'], name='fk_rails_2572a8deee'),
        ForeignKeyConstraint(['parent_page_id'], ['pages.id'], name='fk_rails_de7a57299d'),
        ForeignKeyConstraint(['source_library_page_id'], ['library_pages.id'], name='fk_rails_3f610a52ee'),
        PrimaryKeyConstraint('id', name='pages_pkey'),
        Index('index_pages_on_clip_id', 'clip_id'),
        Index('index_pages_on_journey_id', 'journey_id'),
        Index('index_pages_on_parent_page_id', 'parent_page_id', unique=True),
        Index('index_pages_on_source_library_page_id', 'source_library_page_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String)
    journey_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    heading: Mapped[Optional[str]] = mapped_column(Text)
    order: Mapped[Optional[int]] = mapped_column(Integer)
    minimum: Mapped[Optional[int]] = mapped_column(Integer)
    maximum: Mapped[Optional[int]] = mapped_column(Integer)
    first_name: Mapped[Optional[bool]] = mapped_column(Boolean)
    last_name: Mapped[Optional[bool]] = mapped_column(Boolean)
    phone: Mapped[Optional[bool]] = mapped_column(Boolean)
    email: Mapped[Optional[bool]] = mapped_column(Boolean)
    parent_page_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    company: Mapped[Optional[bool]] = mapped_column(Boolean)
    subtext: Mapped[Optional[str]] = mapped_column(String)
    required: Mapped[Optional[bool]] = mapped_column(Boolean)
    button_text: Mapped[Optional[str]] = mapped_column(String)
    button_url: Mapped[Optional[str]] = mapped_column(String)
    button2_text: Mapped[Optional[str]] = mapped_column(String)
    button2_url: Mapped[Optional[str]] = mapped_column(String)
    consent: Mapped[Optional[bool]] = mapped_column(Boolean)
    consent_text: Mapped[Optional[str]] = mapped_column(String)
    middle_name: Mapped[Optional[bool]] = mapped_column(Boolean)
    consent_required: Mapped[Optional[bool]] = mapped_column(Boolean)
    privilege_required: Mapped[Optional[bool]] = mapped_column(Boolean)
    email_required: Mapped[Optional[bool]] = mapped_column(Boolean)
    phone_required: Mapped[Optional[bool]] = mapped_column(Boolean)
    custom_checkbox: Mapped[Optional[bool]] = mapped_column(Boolean)
    custom_checkbox_required: Mapped[Optional[bool]] = mapped_column(Boolean)
    custom_checkbox_message: Mapped[Optional[str]] = mapped_column(String)
    clip_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    source_library_page_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    clip: Mapped[Optional['Clips']] = relationship('Clips', back_populates='pages')
    journey: Mapped[Optional['Journeys']] = relationship('Journeys', back_populates='pages')
    parent_page: Mapped[Optional['Pages']] = relationship('Pages', remote_side=[id], back_populates='parent_page_reverse')
    parent_page_reverse: Mapped[list['Pages']] = relationship('Pages', remote_side=[parent_page_id], back_populates='parent_page')
    source_library_page: Mapped[Optional['LibraryPages']] = relationship('LibraryPages', back_populates='pages')
    answer_options: Mapped[list['AnswerOptions']] = relationship('AnswerOptions', back_populates='page')
    navigation_rules: Mapped[list['NavigationRules']] = relationship('NavigationRules', back_populates='page')


class AnswerOptions(Base):
    __tablename__ = 'answer_options'
    __table_args__ = (
        ForeignKeyConstraint(['page_id'], ['pages.id'], name='fk_rails_4d660e1508'),
        PrimaryKeyConstraint('id', name='answer_options_pkey'),
        Index('index_answer_options_on_page_id', 'page_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    page_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    body: Mapped[Optional[str]] = mapped_column(Text)
    order: Mapped[Optional[int]] = mapped_column(Integer)

    page: Mapped['Pages'] = relationship('Pages', back_populates='answer_options')
    navigation_rules: Mapped[list['NavigationRules']] = relationship('NavigationRules', back_populates='answer_option')


class AutomationEvents(Base):
    __tablename__ = 'automation_events'
    __table_args__ = (
        ForeignKeyConstraint(['automation_id'], ['automations.id'], name='fk_rails_788a3d3897'),
        ForeignKeyConstraint(['lead_id'], ['leads.id'], name='fk_rails_b1cdd6b9ed'),
        PrimaryKeyConstraint('id', name='automation_events_pkey'),
        Index('index_automation_events_on_automation_id', 'automation_id'),
        Index('index_automation_events_on_automation_token', 'automation_token', unique=True),
        Index('index_automation_events_on_lead_id', 'lead_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    automation_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    lead_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    automation_token: Mapped[Optional[str]] = mapped_column(String)
    schedule_send_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    read_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    skipped: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    details: Mapped[Optional[dict]] = mapped_column(JSONB)

    automation: Mapped['Automations'] = relationship('Automations', back_populates='automation_events')
    lead: Mapped['Leads'] = relationship('Leads', back_populates='automation_events')


class Responses(Base):
    __tablename__ = 'responses'
    __table_args__ = (
        ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE', name='fk_rails_2e83670baa'),
        PrimaryKeyConstraint('id', name='responses_pkey'),
        Index('index_responses_on_lead_id', 'lead_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    lead_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String)
    question_title: Mapped[Optional[str]] = mapped_column(String)
    question_body: Mapped[Optional[str]] = mapped_column(String)
    raw_value: Mapped[Optional[str]] = mapped_column(Text)
    order: Mapped[Optional[int]] = mapped_column(Integer)
    page_type: Mapped[Optional[str]] = mapped_column(String)

    lead: Mapped['Leads'] = relationship('Leads', back_populates='responses')


class SettingsLeadIntegrationStatuses(Base):
    __tablename__ = 'settings_lead_integration_statuses'
    __table_args__ = (
        ForeignKeyConstraint(['lead_id'], ['leads.id'], name='fk_rails_7c8f17a168'),
        ForeignKeyConstraint(['settings_integration_id'], ['settings_integrations.id'], name='fk_rails_3c73b05890'),
        PrimaryKeyConstraint('id', name='settings_lead_integration_statuses_pkey'),
        Index('index_integration_statuses', 'settings_integration_id'),
        Index('index_settings_lead_integration_statuses_on_lead_id', 'lead_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    lead_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    settings_integration_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    status: Mapped[Optional[int]] = mapped_column(Integer)
    message: Mapped[Optional[str]] = mapped_column(Text)

    lead: Mapped['Leads'] = relationship('Leads', back_populates='settings_lead_integration_statuses')
    settings_integration: Mapped['SettingsIntegrations'] = relationship('SettingsIntegrations', back_populates='settings_lead_integration_statuses')


class NavigationRules(Base):
    __tablename__ = 'navigation_rules'
    __table_args__ = (
        ForeignKeyConstraint(['answer_option_id'], ['answer_options.id'], name='fk_rails_aa7e7b5fdb'),
        ForeignKeyConstraint(['page_id'], ['pages.id'], name='fk_rails_a4fb6094b1'),
        PrimaryKeyConstraint('id', name='navigation_rules_pkey'),
        Index('index_navigation_rules_on_answer_option_id', 'answer_option_id'),
        Index('index_navigation_rules_on_page_id', 'page_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    page_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=6), nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String)
    value: Mapped[Optional[str]] = mapped_column(String)
    answer_option_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    answer_option: Mapped[Optional['AnswerOptions']] = relationship('AnswerOptions', back_populates='navigation_rules')
    page: Mapped['Pages'] = relationship('Pages', back_populates='navigation_rules')
