import csv
import gzip
import json
from collections import OrderedDict
from datetime import datetime

from ..db import db, ActiveModel, full_commit


class CampaignFacts(ActiveModel, db.Model):
    __tablename__ = 'campaign_facts'

    # Dimensions
    date = db.Column(db.Date, nullable=False, default=datetime.today, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False, primary_key=True)
    campaign_id = db.Column(db.Integer, nullable=False, primary_key=True)
    campaign = db.Column(db.String(128), nullable=False)
    # Using enum in case there are other acceptable values besides enabled and ended I'm not aware of
    # But those are the only two I saw in the CSV
    campaign_state = db.Column(db.Enum('enabled', 'disabled', name='campaign_states'), nullable=False, default='enabled')
    campaign_serving_status = db.Column(db.Enum('ended', 'running', name='campaign_serving_statuses'), nullable=False, default='enabled')
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)  # Have a feeling this could be NULL
    budget = db.Column(db.Integer, nullable=False)
    budget_id = db.Column(db.Integer, nullable=False)
    budget_explicit_share = db.Column(db.Boolean, nullable=False, default=False)  # Seems False is most common
    # I'm assuming comma separated values for these, although the example only contains empty values
    # IMPORTANT: "The json_typeof function's null return value should not be confused with a SQL NULL.
    # While calling json_typeof('null'::json) will return null, calling json_typeof(NULL::json) will return a SQL NULL."
    # https://www.postgresql.org/docs/9.4/static/functions-json.html#FUNCTIONS-JSON-PROCESSING-TABLE
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

    @staticmethod
    def json_or_null(row):
        if row.strip() == '--':
            return None
        return json.dumps(row)

    @property
    def ctr(self):
        return float(self.clicks) / self.impressions * 100

    @property
    def interaction_rate(self):
        return float(self.interactions) / self.impressions * 100

    @property
    def conversion_rate(self):
        return float(self.conversions) / self.interactions * 100

    @classmethod
    def load_from_gzip_csv(cls, gzip_file, output_gzip_file, with_header=True):
        with gzip.open(gzip_file) as in_f:
            reader = csv.reader(in_f)
            # If header is included in file it should be skipped
            if with_header:
                reader.next()
            with gzip.open(output_gzip_file, 'wt') as out_f:
                writer = csv.writer(out_f)
                for row in reader:
                    facts_row = OrderedDict([
                        ('date', row[0]),
                        ('customer_id', row[1]),
                        ('campaign_id', row[2]),
                        ('campaign', row[3]),
                        ('campaign_state', row[4]),
                        ('campaign_serving_status', row[5]),
                        ('start_date', row[7]),
                        ('end_date', row[8]),
                        ('budget', row[9]),
                        ('budget_id', row[10]),
                        ('budget_explicit_share', False if row[11] == 'false' else True),
                        ('label_ids', cls.json_or_null(row[12])),
                        ('labels', cls.json_or_null(row[13])),
                        ('clicks', int(row[6])),
                        ('invalid_clicks', int(row[14])),
                        ('conversions', int(float(row[15]))),
                        ('cost', int(row[18])),
                        ('impressions', int(row[19])),
                        ('search_lost_is', float(row[20].replace('%', ''))),
                        ('avg_position', float(row[21])),
                        ('interactions', int(row[23]))
                    ])
                    fact = cls(**facts_row)
                    fact.save(commit=False)
                    writer.writerow(facts_row.values())
        try:
            full_commit()
            return True
        except Exception as ex:
            # Should log exception somewhere
            db.session.rollback()

    def __repr__(self):
        return '<Campaign Fact {} {} {}>'.format(self.date, self.customer_id, self.campaign_id)
