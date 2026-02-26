"""
AMSA Configuration Manager
Centralized configuration with environment variables and defaults
"""
import os
from dataclasses import dataclass
from typing import Optional
import logging

@dataclass
class NewsAPIConfig:
    """News API configuration"""
    api_key: str = os.getenv("NEWS_API_KEY", "")
    sources: list = None
    domains: list = None
    
    def __post_init__(self):
        if self.sources is None:
            self.sources = ["bloomberg", "reuters", "financial-times", "cnbc"]
        if self.domains is None:
            self.domains = ["bloomberg.com", "reuters.com", "ft.com", "cnbc.com"]

@dataclass
class TwitterConfig:
    """Twitter/X API configuration"""
    api_key: str = os.getenv("TWITTER_API_KEY", "")
    api_secret: str = os.getenv("TWITTER_API_SECRET", "")
    access_token: str = os.getenv("TWITTER_ACCESS_TOKEN", "")
    access_secret: str = os.getenv("TWITTER_ACCESS_SECRET", "")
    track_keywords: list = None
    
    def __post_init__(self):
        if self.track_keywords is None:
            self.track_keywords = [
                "$SPY", "$QQQ", "$BTC", "stock market", 
                "bull market", "bear market", "Fed", "inflation"
            ]

@dataclass
class FinancialConfig:
    """Financial data configuration"""
    alpha_vantage_key: str = os.getenv("ALPHA_VANTAGE_KEY", "")
    finnhub_key: str = os.getenv("FINNHUB_KEY", "")
    market_watch_url: str = "https://www.marketwatch.com/investing"

@dataclass
class FirebaseConfig:
    """Firebase configuration"""
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "")
    credentials_path: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    database_url: str = os.getenv("FIREBASE_DATABASE_URL", "")

@dataclass
class ModelConfig:
    """ML model configuration"""
    update_interval_hours: int = 6
    min_training_samples: int = 1000
    sentiment_threshold: float = 0.3
    retrain_on_failure: bool = True

class Config:
    """Main configuration class"""
    
    def __init__(self):
        # Initialize configurations
        self.news = NewsAPIConfig()
        self.twitter = TwitterConfig()
        self.financial = FinancialConfig()
        self.firebase = FirebaseConfig()
        self.model = ModelConfig()
        
        # Validate critical configurations
        self._validate_config()
        
    def _validate_config(self) -> None:
        """Validate critical configuration values"""
        missing_configs = []
        
        # Check for required API keys
        if not self.news.api_key:
            missing_configs.append("NEWS_API_KEY")
        if not self.twitter.api_key:
            missing_configs.append("TWITTER_API_KEY")
        if not self.alpha_vantage_key:
            missing_configs.append("ALPHA_VANTAGE_KEY")
        if not self.firebase.project_id:
            missing_configs.append("FIREBASE_PROJECT_ID")
            
        if missing_configs:
            warning_msg = f"Missing configuration: {', '.join(missing_configs)}"
            logging.warning(warning_msg)
            # In production, we might raise an exception
            # For now, we'll log and continue with degraded functionality
    
    @property
    def alpha_vantage_key(self) -> str:
        """Getter for Alpha Vantage key"""
        return self.financial.alpha_vantage_key

# Global configuration instance
config = Config()