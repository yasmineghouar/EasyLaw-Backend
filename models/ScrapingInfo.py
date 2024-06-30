from sqlalchemy import func, Date, Boolean
from datetime import datetime
from ..app import db

class ScrapingInfo(db.Model):
    __tablename__ = "scrapingInfo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service = db.Column(db.String(255))
    autoScraping = db.Column(db.Boolean)  
    lastDate = db.Column(db.Date)  
  
    def __repr__(self):
        return f'<scrapingInfo {self.id}>'



class ScrapingInfoHistory(db.Model):
    __tablename__ = "scraping_info_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scraping_info_id = db.Column(db.Integer, db.ForeignKey('scrapingInfo.id'))
    service = db.Column(db.String(255))
    autoScraping = db.Column(db.Boolean)
    lastDate = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.String(255))  # username or system
    action = db.Column(db.String(255))  # Action performed (e.g., update, toggle_autoScraping)

    def __repr__(self):
        return f'<ScrapingInfoHistory {self.id}>'
