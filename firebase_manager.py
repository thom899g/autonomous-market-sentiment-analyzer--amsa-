"""
Firebase Manager for AMSA
Handles all Firebase operations including data persistence, real-time updates, and state management
"""
import firebase_admin
from firebase_admin import credentials, firestore, db
from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime, timedelta
import time

class FirebaseManager:
    """Firebase management class for storing and retrieving AMSA data"""
    
    # Collection/Path constants
    COLLECTIONS = {
        'sentiment': 'market_sentiment',
        'raw_data': 'raw_collected_data',
        'models': 'active_models',
        'errors': 'system_errors',
        'performance': 'model_performance'
    }
    
    def __init__(self, config):
        """Initialize Firebase connection"""
        self.config = config
        self.app = None
        self.db = None
        self.rtdb = None
        self._initialize_firebase()
        
    def _initialize_firebase(self) -> None:
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate(self.config.firebase.credentials_path)
                self.app = firebase_admin.initialize_app(
                    cred,
                    {
                        'databaseURL': self.config.firebase.database_url,
                        'projectId': self.config.firebase.project_id
                    }
                )
                logging.info("Firebase Admin SDK initialized successfully")
            else:
                self.app