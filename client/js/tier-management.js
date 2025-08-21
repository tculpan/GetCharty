/*
client/js/tier-management.js
Updated: 2025-08-21 23:28:18
Tier detection and validation for GetCharty application
FIXED: Added error handling and fallback for tier class application
*/

// Tier definitions and configuration
const TIER_CONFIG = {
    noob: {
        name: 'Noob',
        features: {
            watermark: true,
            watermarkOpacity: 0.4,
            watermarkSize: 14,
            exportJPG: true,
            autoSpacing: false,
            advancedCharts: false,
            customBranding: false
        },
        limits: {
            monthlyCharts: 10,
            fileSizeMB: 5
        }
    },
    registered: {
        name: 'Registered',
        features: {
            watermark: true,
            watermarkOpacity: 0.4,
            watermarkSize: 14,
            exportJPG: true,
            autoSpacing: true,
            advancedCharts: true,
            customBranding: false
        },
        limits: {
            monthlyCharts: 50,
            fileSizeMB: 10
        }
    },
    viper: {
        name: 'VIPer',
        features: {
            watermark: false,
            watermarkOpacity: 0.2,
            watermarkSize: 12,
            exportJPG: true,
            autoSpacing: true,
            advancedCharts: true,
            customBranding: true
        },
        limits: {
            monthlyCharts: -1, // unlimited
            fileSizeMB: 25
        }
    }
};

// Current tier detection
let currentTier = 'noob';
let sessionId = null;

// Initialize tier management
function initializeTierManagement() {
    try {
        sessionId = localStorage.getItem('getcharty_session_id') || generateSessionId();
        localStorage.setItem('getcharty_session_id', sessionId);
        
        // Detect tier based on user status
        detectUserTier();
        
        // Apply tier-based feature restrictions
        applyTierFeatures();
        
        console.log(`Tier management initialized. Current tier: ${currentTier}`);
    } catch (error) {
        console.error('Error initializing tier management:', error);
        // Fallback: ensure body has a tier class
        document.body.className = 'tier-noob';
    }
}

// Detect user tier based on various factors
function detectUserTier() {
    // Check for VIPer tier (paid users)
    if (isVIPerUser()) {
        currentTier = 'viper';
        return;
    }
    
    // Check for registered tier (free registered users)
    if (isRegisteredUser()) {
        currentTier = 'registered';
        return;
    }
    
    // Default to noob tier
    currentTier = 'noob';
}

// Check if user is VIPer (paid tier)
function isVIPerUser() {
    // TODO: Implement VIPer detection logic
    // This could check for:
    // - Payment status
    // - Subscription tokens
    // - Server-side validation
    return false;
}

// Check if user is registered (free tier)
function isRegisteredUser() {
    // TODO: Implement registered user detection
    // This could check for:
    // - Email verification
    // - Account creation
    // - Server-side validation
    return false;
}

// Apply tier-based feature restrictions
function applyTierFeatures() {
    const config = TIER_CONFIG[currentTier];
    
    // Apply watermark settings
    if (typeof window.applyWatermarkSettings === 'function') {
        window.applyWatermarkSettings(config.features);
    }
    
    // Apply feature restrictions
    applyFeatureRestrictions(config.features);
    
    // Update UI based on tier
    updateTierUI();
}

// Apply feature restrictions based on tier
function applyFeatureRestrictions(features) {
    // Auto-spacing feature
    const autoSpacingToggle = document.getElementById('autoSpacing');
    if (autoSpacingToggle) {
        autoSpacingToggle.disabled = !features.autoSpacing;
        if (!features.autoSpacing) {
            autoSpacingToggle.checked = false;
        }
    }
    
    // Advanced chart types
    const advancedChartButtons = document.querySelectorAll('[data-chart-type="advanced"]');
    advancedChartButtons.forEach(btn => {
        btn.style.display = features.advancedCharts ? 'flex' : 'none';
    });
    
    // Custom branding options
    const brandingOptions = document.querySelectorAll('.branding-option');
    brandingOptions.forEach(option => {
        option.style.display = features.customBranding ? 'block' : 'none';
    });
}

// Update UI elements based on current tier
function updateTierUI() {
    const tierName = TIER_CONFIG[currentTier].name;
    
    // Apply tier class to body
    document.body.className = `tier-${currentTier}`;
    
    // Update tier progression bar
    updateTierProgressionBar();
    
    // Update tier labels
    updateTierLabels();
    
    // Show/hide tier-specific elements
    updateTierSpecificElements();
    
    // Update export interface for new tier
    if (window.exportInterface && typeof window.exportInterface.updateForTier === 'function') {
        window.exportInterface.updateForTier(currentTier);
    }
}

// Update tier progression bar
function updateTierProgressionBar() {
    const usageFill = document.querySelector('.usage-fill');
    if (usageFill) {
        let progress = 0;
        switch (currentTier) {
            case 'noob':
                progress = 25;
                break;
            case 'registered':
                progress = 60;
                break;
            case 'viper':
                progress = 100;
                break;
        }
        usageFill.style.width = `${progress}%`;
    }
}

// Update tier labels
function updateTierLabels() {
    const tierLabels = document.querySelectorAll('.tier-noob, .tier-registered, .tier-viper');
    tierLabels.forEach(label => {
        label.classList.remove('active');
    });
    
    const currentTierLabel = document.querySelector(`.tier-${currentTier}`);
    if (currentTierLabel) {
        currentTierLabel.classList.add('active');
    }
}

// Update tier-specific UI elements
function updateTierSpecificElements() {
    // Show/hide velvet curtain button based on tier
    const velvetCurtainBtn = document.querySelector('.velvet-curtain-btn');
    if (velvetCurtainBtn) {
        velvetCurtainBtn.style.display = currentTier === 'noob' ? 'block' : 'none';
    }
    
    // Update watermark text in chart container
    updateWatermarkText();
    
    // Update registration messages
    updateRegistrationMessages();
}

// Update watermark text in chart container
function updateWatermarkText() {
    const watermarkNote = document.querySelector('.watermark-note');
    if (watermarkNote) {
        if (currentTier === 'viper') {
            watermarkNote.textContent = 'No watermark!';
        } else {
            watermarkNote.textContent = 'Includes GetCharty.com Watermark';
        }
    }
}

// Update registration messages
function updateRegistrationMessages() {
    const messages = document.querySelectorAll('.registration-message');
    messages.forEach(message => {
        if (currentTier === 'noob') {
            message.style.display = 'block';
            message.textContent = 'Upgrade to Registered for this feature';
        } else if (currentTier === 'registered') {
            message.style.display = 'block';
            message.textContent = 'Upgrade to VIPer for this feature';
        } else {
            message.style.display = 'none';
        }
    });
}

// Get current tier configuration
function getCurrentTierConfig() {
    return TIER_CONFIG[currentTier];
}

// Check if a feature is available for current tier
function isFeatureAvailable(featureName) {
    const config = getCurrentTierConfig();
    return config.features[featureName] || false;
}

// Get feature value for current tier
function getFeatureValue(featureName) {
    const config = getCurrentTierConfig();
    return config.features[featureName];
}

// Track usage for current tier
function trackUsage(action) {
    const config = getCurrentTierConfig();
    
    // TODO: Implement usage tracking
    // This could:
    // - Send usage data to server
    // - Update local storage
    // - Check against monthly limits
    
    console.log(`Usage tracked: ${action} for tier ${currentTier}`);
}

// Generate session ID
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Export functions for use in other modules
window.tierManagement = {
    initialize: initializeTierManagement,
    getCurrentTier: () => currentTier,
    getCurrentTierConfig: getCurrentTierConfig,
    isFeatureAvailable: isFeatureAvailable,
    getFeatureValue: getFeatureValue,
    trackUsage: trackUsage
};
