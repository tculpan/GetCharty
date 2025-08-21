"""
server/tier_management.py
Updated: 2025-08-21 14:24:37
Tier management and validation for GetCharty server
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import hashlib
import ipaddress

class TierManager:
    """Manages user tiers and feature access"""
    
    def __init__(self, config_path: str = "config/tiers.json"):
        self.config_path = config_path
        self.tier_config = self._load_tier_config()
        self.user_sessions = {}  # In-memory session storage
        self.ip_usage = {}       # IP-based usage tracking
        
    def _load_tier_config(self) -> Dict:
        """Load tier configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default configuration if file not found
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default tier configuration"""
        return {
            "tiers": {
                "noob": {
                    "name": "Noob",
                    "features": {
                        "watermark": True,
                        "watermarkOpacity": 0.4,
                        "watermarkSize": 14,
                        "exportJPG": True,
                        "autoSpacing": False,
                        "advancedCharts": False,
                        "customBranding": False
                    },
                    "limits": {
                        "monthlyCharts": 10,
                        "fileSizeMB": 5
                    }
                },
                "registered": {
                    "name": "Registered",
                    "features": {
                        "watermark": True,
                        "watermarkOpacity": 0.4,
                        "watermarkSize": 14,
                        "exportJPG": True,
                        "autoSpacing": True,
                        "advancedCharts": True,
                        "customBranding": False
                    },
                    "limits": {
                        "monthlyCharts": 50,
                        "fileSizeMB": 10
                    }
                },
                "viper": {
                    "name": "VIPer",
                    "features": {
                        "watermark": False,
                        "watermarkOpacity": 0.2,
                        "watermarkSize": 12,
                        "exportJPG": True,
                        "autoSpacing": True,
                        "advancedCharts": True,
                        "customBranding": True
                    },
                    "limits": {
                        "monthlyCharts": -1,
                        "fileSizeMB": 25
                    }
                }
            }
        }
    
    def detect_user_tier(self, session_id: str, ip_address: str, 
                        user_token: Optional[str] = None) -> str:
        """Detect user tier based on session, IP, and token"""
        
        # Check for VIPer tier (paid users)
        if user_token and self._validate_viper_token(user_token):
            return "viper"
        
        # Check for registered tier (free registered users)
        if user_token and self._validate_registered_token(user_token):
            return "registered"
        
        # Check IP-based usage for noob tier
        if self._check_ip_usage_limits(ip_address):
            return "noob"
        
        # Default to noob tier
        return "noob"
    
    def _validate_viper_token(self, token: str) -> bool:
        """Validate VIPer subscription token"""
        # TODO: Implement actual token validation
        # This could check against a payment processor or database
        return False
    
    def _validate_registered_token(self, token: str) -> bool:
        """Validate registered user token"""
        # TODO: Implement actual token validation
        # This could check against user database
        return False
    
    def _check_ip_usage_limits(self, ip_address: str) -> bool:
        """Check if IP address has exceeded usage limits"""
        current_time = time.time()
        current_month = datetime.now().strftime("%Y-%m")
        
        # Clean up old usage data
        self._cleanup_old_usage()
        
        # Get usage for current month
        usage_key = f"{ip_address}:{current_month}"
        usage = self.ip_usage.get(usage_key, {"charts": 0, "last_used": 0})
        
        # Check if within limits (10 charts per month for noob tier)
        return usage["charts"] < 10
    
    def _cleanup_old_usage(self):
        """Clean up usage data older than 3 months"""
        current_time = time.time()
        cutoff_time = current_time - (90 * 24 * 60 * 60)  # 90 days
        
        keys_to_remove = []
        for key, usage in self.ip_usage.items():
            if usage["last_used"] < cutoff_time:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.ip_usage[key]
    
    def track_usage(self, session_id: str, ip_address: str, action: str):
        """Track user usage for tier enforcement"""
        current_time = time.time()
        current_month = datetime.now().strftime("%Y-%m")
        
        # Track IP-based usage
        usage_key = f"{ip_address}:{current_month}"
        if usage_key not in self.ip_usage:
            self.ip_usage[usage_key] = {"charts": 0, "last_used": current_time}
        
        if action == "generate_chart":
            self.ip_usage[usage_key]["charts"] += 1
            self.ip_usage[usage_key]["last_used"] = current_time
        
        # Track session usage
        if session_id not in self.user_sessions:
            self.user_sessions[session_id] = {
                "ip_address": ip_address,
                "created": current_time,
                "last_used": current_time,
                "actions": []
            }
        
        self.user_sessions[session_id]["last_used"] = current_time
        self.user_sessions[session_id]["actions"].append({
            "action": action,
            "timestamp": current_time
        })
    
    def get_tier_config(self, tier: str) -> Dict:
        """Get configuration for a specific tier"""
        return self.tier_config["tiers"].get(tier, {})
    
    def is_feature_available(self, tier: str, feature: str) -> bool:
        """Check if a feature is available for a tier"""
        tier_config = self.get_tier_config(tier)
        return tier_config.get("features", {}).get(feature, False)
    
    def get_feature_value(self, tier: str, feature: str):
        """Get the value of a feature for a tier"""
        tier_config = self.get_tier_config(tier)
        return tier_config.get("features", {}).get(feature)
    
    def check_usage_limit(self, tier: str, ip_address: str, action: str) -> bool:
        """Check if user has exceeded usage limits"""
        tier_config = self.get_tier_config(tier)
        limits = tier_config.get("limits", {})
        
        if action == "generate_chart":
            monthly_limit = limits.get("monthlyCharts", -1)
            if monthly_limit == -1:  # Unlimited
                return True
            
            current_month = datetime.now().strftime("%Y-%m")
            usage_key = f"{ip_address}:{current_month}"
            current_usage = self.ip_usage.get(usage_key, {"charts": 0})
            
            return current_usage["charts"] < monthly_limit
        
        return True
    
    def get_usage_stats(self, ip_address: str) -> Dict:
        """Get usage statistics for an IP address"""
        current_month = datetime.now().strftime("%Y-%m")
        usage_key = f"{ip_address}:{current_month}"
        usage = self.ip_usage.get(usage_key, {"charts": 0, "last_used": 0})
        
        return {
            "current_month": current_month,
            "charts_generated": usage["charts"],
            "last_used": datetime.fromtimestamp(usage["last_used"]).isoformat() if usage["last_used"] > 0 else None
        }
    
    def validate_file_size(self, tier: str, file_size_mb: float) -> bool:
        """Validate if file size is within tier limits"""
        tier_config = self.get_tier_config(tier)
        max_size = tier_config.get("limits", {}).get("fileSizeMB", 5)
        return file_size_mb <= max_size
    
    def get_upgrade_info(self, current_tier: str) -> Dict:
        """Get upgrade information for current tier"""
        upgrades = self.tier_config.get("upgrades", {})
        
        if current_tier == "noob":
            return upgrades.get("noob_to_registered", {})
        elif current_tier == "registered":
            return upgrades.get("registered_to_viper", {})
        
        return {}

# Global tier manager instance
tier_manager = TierManager()

# Convenience functions for Flask integration
def get_user_tier(session_id: str, ip_address: str, user_token: Optional[str] = None) -> str:
    """Get user tier for Flask routes"""
    return tier_manager.detect_user_tier(session_id, ip_address, user_token)

def track_user_usage(session_id: str, ip_address: str, action: str):
    """Track user usage for Flask routes"""
    tier_manager.track_usage(session_id, ip_address, action)

def check_feature_access(tier: str, feature: str) -> bool:
    """Check feature access for Flask routes"""
    return tier_manager.is_feature_available(tier, feature)

def get_tier_features(tier: str) -> Dict:
    """Get all features for a tier"""
    return tier_manager.get_tier_config(tier).get("features", {})
