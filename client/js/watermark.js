/*
client/js/watermark.js
Updated: 2025-08-21 14:24:37
Watermark functionality for GetCharty application
*/

// Watermark configuration
let watermarkConfig = {
    enabled: true,
    text: 'GetCharty.com',
    opacity: 0.4,
    size: 14,
    position: 'bottom-left',
    color: 'rgba(255, 255, 255, 0.4)',
    fontFamily: 'Arial, sans-serif',
    fontWeight: 'bold'
};

// Watermark element reference
let watermarkElement = null;

// Initialize watermark system
function initializeWatermark() {
    console.log('Watermark system initialized');
    
    // Create watermark element if it doesn't exist
    if (!watermarkElement) {
        createWatermarkElement();
    }
    
    // Apply initial watermark settings
    applyWatermarkSettings(watermarkConfig);
}

// Create watermark element
function createWatermarkElement() {
    watermarkElement = document.createElement('div');
    watermarkElement.id = 'chart-watermark';
    watermarkElement.className = 'chart-watermark';
    watermarkElement.textContent = watermarkConfig.text;
    
    // Add watermark to chart container
    const chartContainer = document.getElementById('chartContainer');
    if (chartContainer) {
        chartContainer.appendChild(watermarkElement);
    }
    
    console.log('Watermark element created');
}

// Apply watermark settings
function applyWatermarkSettings(config) {
    watermarkConfig = { ...watermarkConfig, ...config };
    
    if (!watermarkElement) {
        createWatermarkElement();
    }
    
    // Update watermark element styles
    updateWatermarkStyles();
    
    // Show/hide watermark based on enabled status
    if (watermarkElement) {
        watermarkElement.style.display = watermarkConfig.enabled ? 'block' : 'none';
    }
    
    console.log('Watermark settings applied:', watermarkConfig);
}

// Update watermark element styles
function updateWatermarkStyles() {
    if (!watermarkElement) return;
    
    const styles = {
        position: 'absolute',
        color: watermarkConfig.color,
        fontSize: `${watermarkConfig.size}px`,
        fontFamily: watermarkConfig.fontFamily,
        fontWeight: watermarkConfig.fontWeight,
        pointerEvents: 'none',
        zIndex: '1000',
        userSelect: 'none',
        textShadow: '1px 1px 2px rgba(0,0,0,0.5)'
    };
    
    // Position watermark
    switch (watermarkConfig.position) {
        case 'bottom-left':
            styles.bottom = '15px';
            styles.left = '15px';
            break;
        case 'bottom-right':
            styles.bottom = '15px';
            styles.right = '15px';
            break;
        case 'top-left':
            styles.top = '15px';
            styles.left = '15px';
            break;
        case 'top-right':
            styles.top = '15px';
            styles.right = '15px';
            break;
        case 'center':
            styles.top = '50%';
            styles.left = '50%';
            styles.transform = 'translate(-50%, -50%)';
            styles.fontSize = `${watermarkConfig.size * 2}px`;
            styles.opacity = '0.1';
            break;
    }
    
    // Apply styles to watermark element
    Object.assign(watermarkElement.style, styles);
}

// Add watermark to canvas for export
function addWatermarkToCanvas(canvas, options = {}) {
    const ctx = canvas.getContext('2d');
    const config = { ...watermarkConfig, ...options };
    
    if (!config.enabled) return canvas;
    
    // Set watermark text properties
    ctx.font = `${config.fontWeight} ${config.size}px ${config.fontFamily}`;
    ctx.fillStyle = config.color;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'bottom';
    
    // Calculate position
    let x, y;
    const padding = 20;
    
    switch (config.position) {
        case 'bottom-left':
            x = padding;
            y = canvas.height - padding;
            break;
        case 'bottom-right':
            x = canvas.width - padding;
            y = canvas.height - padding;
            ctx.textAlign = 'right';
            break;
        case 'top-left':
            x = padding;
            y = padding + config.size;
            break;
        case 'top-right':
            x = canvas.width - padding;
            y = padding + config.size;
            ctx.textAlign = 'right';
            break;
        case 'center':
            x = canvas.width / 2;
            y = canvas.height / 2;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.font = `${config.fontWeight} ${config.size * 2}px ${config.fontFamily}`;
            ctx.globalAlpha = 0.1;
            break;
    }
    
    // Add text shadow for better visibility
    ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
    ctx.shadowBlur = 2;
    ctx.shadowOffsetX = 1;
    ctx.shadowOffsetY = 1;
    
    // Draw watermark text
    ctx.fillText(config.text, x, y);
    
    // Reset shadow
    ctx.shadowColor = 'transparent';
    ctx.shadowBlur = 0;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;
    ctx.globalAlpha = 1;
    
    console.log('Watermark added to canvas');
    return canvas;
}

// Remove watermark element
function removeWatermark() {
    if (watermarkElement && watermarkElement.parentNode) {
        watermarkElement.parentNode.removeChild(watermarkElement);
        watermarkElement = null;
    }
}

// Update watermark position when chart container changes
function updateWatermarkPosition() {
    if (watermarkElement) {
        updateWatermarkStyles();
    }
}

// Get current watermark configuration
function getWatermarkConfig() {
    return { ...watermarkConfig };
}

// Set watermark text
function setWatermarkText(text) {
    watermarkConfig.text = text;
    if (watermarkElement) {
        watermarkElement.textContent = text;
    }
}

// Set watermark opacity
function setWatermarkOpacity(opacity) {
    watermarkConfig.opacity = opacity;
    watermarkConfig.color = `rgba(255, 255, 255, ${opacity})`;
    updateWatermarkStyles();
}

// Set watermark size
function setWatermarkSize(size) {
    watermarkConfig.size = size;
    updateWatermarkStyles();
}

// Set watermark position
function setWatermarkPosition(position) {
    watermarkConfig.position = position;
    updateWatermarkStyles();
}

// Enable/disable watermark
function setWatermarkEnabled(enabled) {
    watermarkConfig.enabled = enabled;
    if (watermarkElement) {
        watermarkElement.style.display = enabled ? 'block' : 'none';
    }
}

// Export functions for use in other modules
window.watermark = {
    initialize: initializeWatermark,
    applySettings: applyWatermarkSettings,
    addToCanvas: addWatermarkToCanvas,
    remove: removeWatermark,
    updatePosition: updateWatermarkPosition,
    getConfig: getWatermarkConfig,
    setText: setWatermarkText,
    setOpacity: setWatermarkOpacity,
    setSize: setWatermarkSize,
    setPosition: setWatermarkPosition,
    setEnabled: setWatermarkEnabled
};

// Global function for tier management integration
window.applyWatermarkSettings = applyWatermarkSettings;
