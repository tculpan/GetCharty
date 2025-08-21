/*
client/js/export-handlers.js
Updated: 2025-08-21 14:24:37
Export functionality for GetCharty application
*/

// Export configuration
let exportConfig = {
    format: 'jpg',
    quality: 0.9,
    scale: 2, // Higher scale for better quality
    backgroundColor: '#000000'
};

// html2canvas library reference
let html2canvas = null;

// Initialize export system
async function initializeExport() {
    console.log('Export system initializing...');
    
    // Load html2canvas library dynamically
    await loadHtml2Canvas();
    
    console.log('Export system initialized');
}

// Load html2canvas library
async function loadHtml2Canvas() {
    if (html2canvas) return html2canvas;
    
    try {
        // Load html2canvas from CDN
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
        script.async = true;
        
        await new Promise((resolve, reject) => {
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
        
        html2canvas = window.html2canvas;
        console.log('html2canvas loaded successfully');
        
    } catch (error) {
        console.error('Failed to load html2canvas:', error);
        throw new Error('Export functionality unavailable');
    }
}

// Export chart as JPG
async function exportChartAsJPG(options = {}) {
    try {
        // Check if chart exists
        const chartContainer = document.getElementById('chartContainer');
        if (!chartContainer) {
            throw new Error('No chart container found');
        }
        
        // Check if chart has been generated
        const plotlyChart = document.getElementById('plotlyChart');
        if (!plotlyChart || plotlyChart.children.length === 0) {
            throw new Error('No chart to export. Please generate a chart first.');
        }
        
        // Ensure html2canvas is loaded
        await loadHtml2Canvas();
        
        // Get tier-based watermark settings
        const tierConfig = window.tierManagement ? window.tierManagement.getCurrentTierConfig() : null;
        const watermarkSettings = tierConfig ? tierConfig.features : { watermark: true, watermarkOpacity: 0.4, watermarkSize: 14 };
        
        // Capture chart container
        const canvas = await html2canvas(chartContainer, {
            scale: exportConfig.scale,
            useCORS: true,
            allowTaint: true,
            backgroundColor: exportConfig.backgroundColor,
            width: chartContainer.offsetWidth,
            height: chartContainer.offsetHeight,
            scrollX: 0,
            scrollY: 0,
            windowWidth: document.documentElement.offsetWidth,
            windowHeight: document.documentElement.offsetHeight
        });
        
        // Add watermark to canvas if enabled
        if (window.watermark && watermarkSettings.watermark) {
            window.watermark.addToCanvas(canvas, {
                enabled: watermarkSettings.watermark,
                opacity: watermarkSettings.watermarkOpacity,
                size: watermarkSettings.watermarkSize,
                position: 'bottom-left'
            });
        }
        
        // Convert canvas to JPG
        const jpgDataUrl = canvas.toDataURL('image/jpeg', exportConfig.quality);
        
        // Generate filename
        const filename = generateExportFilename('jpg');
        
        // Trigger download
        downloadFile(jpgDataUrl, filename);
        
        // Track usage
        if (window.tierManagement) {
            window.tierManagement.trackUsage('export_jpg');
        }
        
        console.log('Chart exported as JPG successfully');
        return { success: true, filename };
        
    } catch (error) {
        console.error('Export failed:', error);
        throw error;
    }
}

// Generate export filename
function generateExportFilename(extension) {
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    const chartTitle = document.getElementById('chartTitle')?.value || 'chart';
    const cleanTitle = chartTitle.replace(/[^a-zA-Z0-9\s-]/g, '').replace(/\s+/g, '-').toLowerCase();
    
    return `getcharty-${cleanTitle}-${timestamp}.${extension}`;
}

// Download file from data URL
function downloadFile(dataUrl, filename) {
    const link = document.createElement('a');
    link.href = dataUrl;
    link.download = filename;
    link.style.display = 'none';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Set export quality
function setExportQuality(quality) {
    exportConfig.quality = Math.max(0.1, Math.min(1.0, quality));
}

// Set export scale
function setExportScale(scale) {
    exportConfig.scale = Math.max(1, Math.min(4, scale));
}

// Set export background color
function setExportBackgroundColor(color) {
    exportConfig.backgroundColor = color;
}

// Get export configuration
function getExportConfig() {
    return { ...exportConfig };
}

// Check if export is available
function isExportAvailable() {
    return html2canvas !== null;
}

// Export with custom settings
async function exportWithCustomSettings(settings = {}) {
    const customConfig = { ...exportConfig, ...settings };
    const originalConfig = { ...exportConfig };
    
    // Temporarily apply custom settings
    Object.assign(exportConfig, customConfig);
    
    try {
        const result = await exportChartAsJPG();
        return result;
    } finally {
        // Restore original settings
        Object.assign(exportConfig, originalConfig);
    }
}

// Export with watermark disabled (for testing)
async function exportWithoutWatermark() {
    return await exportWithCustomSettings({
        watermark: false
    });
}

// Export with high quality settings
async function exportHighQuality() {
    return await exportWithCustomSettings({
        quality: 1.0,
        scale: 3
    });
}

// Export with low quality settings (for faster export)
async function exportLowQuality() {
    return await exportWithCustomSettings({
        quality: 0.7,
        scale: 1
    });
}

// Export functions for use in other modules
window.exportHandlers = {
    initialize: initializeExport,
    exportJPG: exportChartAsJPG,
    setQuality: setExportQuality,
    setScale: setExportScale,
    setBackgroundColor: setExportBackgroundColor,
    getConfig: getExportConfig,
    isAvailable: isExportAvailable,
    exportCustom: exportWithCustomSettings,
    exportNoWatermark: exportWithoutWatermark,
    exportHighQuality: exportHighQuality,
    exportLowQuality: exportLowQuality
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeExport);
} else {
    initializeExport();
}
