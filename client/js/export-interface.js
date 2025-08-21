/*
client/js/export-interface.js
Updated: 2025-08-21 14:24:37
Export interface functionality for GetCharty application
*/

// Export interface management
class ExportInterface {
    constructor() {
        this.currentTab = 'export';
        this.currentTier = 'noob';
        this.initialize();
    }

    initialize() {
        console.log('Export interface initializing...');
        this.createExportInterface();
        this.bindEvents();
        console.log('Export interface initialized');
    }

    createExportInterface() {
        // Find the existing export interface container
        const exportContainer = document.getElementById('exportInterfaceContainer');
        if (!exportContainer) {
            console.warn('Export interface container not found');
            return;
        }

        // Create the export interface HTML
        const exportHTML = this.generateExportHTML();
        exportContainer.innerHTML = exportHTML;
    }

    generateExportHTML() {
        return `
            <div class="export-row">
                <div class="export-tabs">
                    <div class="export-tab active" data-tab="export">
                        <span>⬇️</span>
                        <span>Export</span>
                    </div>
                    <div class="export-tab" data-tab="share">
                        <span>🔗</span>
                        <span>Share</span>
                    </div>
                </div>
                
                <div class="export-tab-content active" data-tab="export">
                    <div class="export-tab-buttons">
                        ${this.generateExportButtons()}
                    </div>
                    ${this.generateUpgradePrompt()}
                </div>
                
                <div class="export-tab-content" data-tab="share">
                    <div class="export-tab-buttons">
                        ${this.generateShareButtons()}
                    </div>
                    ${this.generateUpgradePrompt()}
                </div>
            </div>
        `;
    }

    generateExportButtons() {
        const buttons = [
            { id: 'jpg', icon: '📷', label: 'JPG', quality: this.getQualityLabel(), available: true },
            { id: 'pdf', icon: '📄', label: 'PDF', quality: '', available: this.currentTier !== 'noob' },
            { id: 'html', icon: '🌐', label: 'HTML', quality: '', available: this.currentTier !== 'noob' },
            { id: 'svg', icon: '🎨', label: 'SVG', quality: '', available: this.currentTier === 'viper' },
            { id: 'png', icon: '🖼️', label: 'PNG', quality: '', available: this.currentTier === 'viper' }
        ];

        return buttons.map(btn => {
            const lockedClass = !btn.available ? 'locked' : '';
            const viperClass = btn.id === 'svg' || btn.id === 'png' ? 'viper' : '';
            const premiumClass = this.currentTier === 'viper' ? 'premium' : '';
            
            return `
                <button class="export-btn ${lockedClass} ${viperClass} ${premiumClass}" 
                        data-format="${btn.id}" 
                        onclick="exportInterface.handleExport('${btn.id}')">
                    <span class="icon">${btn.icon}</span>
                    <span>${btn.label}</span>
                    ${btn.quality ? `<span class="quality">${btn.quality}</span>` : ''}
                </button>
            `;
        }).join('');
    }

    generateShareButtons() {
        const buttons = [
            { id: 'socials', icon: '📱', label: 'Socials', available: true },
            { id: 'permalink', icon: '🔗', label: 'Permalink', available: this.currentTier !== 'noob' },
            { id: 'email', icon: '📧', label: 'Email', available: this.currentTier === 'viper' }
        ];

        return buttons.map(btn => {
            const lockedClass = !btn.available ? 'locked' : '';
            const viperClass = btn.id === 'email' ? 'viper' : '';
            const premiumClass = this.currentTier === 'viper' ? 'premium' : '';
            
            return `
                <button class="export-btn ${lockedClass} ${viperClass} ${premiumClass}" 
                        data-format="${btn.id}" 
                        onclick="exportInterface.handleExport('${btn.id}')">
                    <span class="icon">${btn.icon}</span>
                    <span>${btn.label}</span>
                </button>
            `;
        }).join('');
    }

    generateUpgradePrompt() {
        if (this.currentTier === 'viper') {
            return '';
        }

        const messages = {
            noob: '📈 Register for Free to get PDF & HTML exports',
            registered: '✨ Upgrade to VIPer for SVG & PNG exports, custom coloring, and much more'
        };

        const upgradeFunction = this.currentTier === 'noob' ? 'upgradeToRegistered()' : 'upgradeToViper()';

        return `
            <div class="upgrade-prompt" onclick="${upgradeFunction}">
                ${messages[this.currentTier]}
            </div>
        `;
    }

    getQualityLabel() {
        const qualities = {
            noob: '720p',
            registered: '1080p',
            viper: '4K'
        };
        return qualities[this.currentTier] || '720p';
    }

    bindEvents() {
        // Tab switching
        document.addEventListener('click', (e) => {
            if (e.target.closest('.export-tab')) {
                const tab = e.target.closest('.export-tab');
                const tabName = tab.dataset.tab;
                this.switchTab(tabName);
            }
        });
    }

    switchTab(tabName) {
        const container = document.querySelector('.export-row');
        if (!container) return;

        // Update tab states
        container.querySelectorAll('.export-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabName);
        });

        // Update content states
        container.querySelectorAll('.export-tab-content').forEach(content => {
            content.classList.toggle('active', content.dataset.tab === tabName);
        });

        this.currentTab = tabName;
    }

    updateForTier(tier) {
        this.currentTier = tier;
        
        // Recreate the interface with new tier settings
        const existingInterface = document.querySelector('.export-interface-container');
        if (existingInterface) {
            existingInterface.remove();
        }
        
        this.createExportInterface();
        this.bindEvents();
    }

    handleExport(format) {
        // Check if the format is available for current tier
        if (!this.isFormatAvailable(format)) {
            this.showUpgradePrompt(format);
            return;
        }

        // Handle different export types
        switch (format) {
            case 'jpg':
            case 'pdf':
            case 'html':
            case 'svg':
            case 'png':
                this.handleFileExport(format);
                break;
            case 'socials':
                this.handleSocialShare();
                break;
            case 'permalink':
                this.handlePermalink();
                break;
            case 'email':
                this.handleEmailShare();
                break;
            default:
                console.warn('Unknown export format:', format);
        }
    }

    isFormatAvailable(format) {
        const availability = {
            noob: ['jpg', 'socials'],
            registered: ['jpg', 'pdf', 'html', 'socials', 'permalink'],
            viper: ['jpg', 'pdf', 'html', 'svg', 'png', 'socials', 'permalink', 'email']
        };

        return availability[this.currentTier]?.includes(format) || false;
    }

    showUpgradePrompt(format) {
        const requiredTier = this.getRequiredTier(format);
        const tierNames = {
            registered: 'Registered',
            viper: 'VIPer'
        };
        
        alert(`✦ ${format.toUpperCase()} export requires ${tierNames[requiredTier]} membership.\n\nUpgrade now to unlock this feature!`);
    }

    getRequiredTier(format) {
        const requirements = {
            pdf: 'registered',
            html: 'registered',
            permalink: 'registered',
            svg: 'viper',
            png: 'viper',
            email: 'viper'
        };
        return requirements[format] || 'registered';
    }

    handleFileExport(format) {
        if (window.exportHandlers && window.exportHandlers.exportJPG) {
            // Use the existing export handler
            window.exportHandlers.exportJPG();
        } else {
            // Fallback
            const quality = this.getQualityLabel();
            alert(`📊 ${this.currentTier.charAt(0).toUpperCase() + this.currentTier.slice(1)} Export: ${format.toUpperCase()}\n\nQuality: ${quality}\n${this.currentTier === 'viper' ? 'No watermark!' : 'Includes watermark'}`);
        }
    }

    handleSocialShare() {
        const messages = {
            noob: '📱 Social Sharing (Noob)\n\nShare your chart on:\n✅ Twitter (with watermark)\n✅ Facebook (with watermark)\n✦ LinkedIn (Requires Registered)\n✦ Instagram (Requires VIPer)',
            registered: '📱 Social Sharing (Registered)\n\nShare your chart on:\n✅ Twitter (reduced watermark)\n✅ Facebook (reduced watermark)\n✅ LinkedIn (reduced watermark)\n✦ Instagram Stories (Requires VIPer)\n✦ Custom formats (Requires VIPer)',
            viper: '✨ Premium Social Sharing (VIPer)\n\nShare your chart on:\n✅ All platforms (minimal watermark)\n✅ Custom branded posts\n✅ Scheduled posting\n✅ Analytics tracking'
        };
        
        alert(messages[this.currentTier]);
    }

    handlePermalink() {
        alert('🔗 Permalink Sharing\n\nGenerate a shareable link to your chart that others can view and interact with.');
    }

    handleEmailShare() {
        alert('📧 Email Sharing\n\nSend your chart directly via email with custom branding and analytics tracking.');
    }

    show() {
        const exportContainer = document.getElementById('exportInterfaceContainer');
        if (exportContainer) {
            exportContainer.style.display = 'block';
        }
    }

    hide() {
        const exportContainer = document.getElementById('exportInterfaceContainer');
        if (exportContainer) {
            exportContainer.style.display = 'none';
        }
    }

    updateForTier(tier) {
        this.currentTier = tier;
        this.createExportInterface();
        this.bindEvents();
    }
}

// Global functions for upgrade prompts
function upgradeToRegistered() {
    alert('🚀 Redirecting to registration page...\n\nRegister for free to unlock PDF, HTML exports and sharing features!');
}

function upgradeToViper() {
    alert('👑 Redirecting to VIPer upgrade page...\n\nGet premium exports, advanced sharing, and professional features!');
}

// Initialize export interface
let exportInterface;

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        exportInterface = new ExportInterface();
    });
} else {
    exportInterface = new ExportInterface();
}

// Export for use in other modules
window.exportInterface = exportInterface;
