from datetime import datetime

from ..db import db, ActiveModel


class CampaignFacts(ActiveModel, db.Model):
    __tablename__ = 'campaign_facts'

    # Dimensions
    date = db.Column(db.Date, nullable=False, default=datetime.today, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False, primary_key=True)
    campaign_id = db.Column(db.Integer, nullable=False, primary_key=True)
    campaign = db.Column(db.String(128), nullable=False)
    # Using enum in case there are other acceptable values besides enabled and disabled I'm not aware of
    campaign_state = db.Column(db.Enum('enabled', 'disabled', name='campaign_states'), nullable=False, default='enabled')
    campaign_serving_status = db.Column(db.Enum('enabled', 'disabled', name='campaign_serving_statuses'), nullable=False, default='enabled')
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)  # Have a feeling this could be NULL
    budget = db.Column(db.Integer, nullable=False)
    budget_id = db.Column(db.Integer, nullable=False)
    budget_explicit_share = db.Column(db.Boolean, nullable=False, default=False)  # Seems False is most common
    label_ids = db.Column(db.JSON)  # JSON array of ids e.g. [1,2,3]
    labels = db.Column(db.JSON)  # JSON array of label names e.g. ['Label One', 'Label Two']

    # Metrics
    clicks = db.Column(db.Integer)
    invalid_clicks = db.Column(db.Integer)
    conversions = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    impressions = db.Column(db.Integer)
    search_lost_is = db.Column(db.Float)
    avg_position = db.Column(db.Float)
    interactions = db.Column(db.Integer)

    # Relationships
    # N/A for this projects

    @property
    def ctr(self):
        return self.clicks / self.impressions * 100

    @property
    def interaction_rate(self):
        return self.interactions / self.impressions * 100

    @property
    def conversion_rate(self):
        return self.conversions / self.interactions * 100
