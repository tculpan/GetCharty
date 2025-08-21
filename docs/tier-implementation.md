# Tier Implementation Guide

**Filename:** docs/tier-implementation.md  
**Updated:** 2025-08-21 14:24:37  
**Description:** Implementation guide for GetCharty tiered membership system

## Overview

GetCharty implements a three-tier membership system:
- **Noob**: Anonymous users with basic features
- **Registered**: Free registered users with enhanced features  
- **VIPer**: Paid users with premium features

## Architecture

### Client-Side Components

#### 1. Tier Management (`client/js/tier-management.js`)
- Tier detection and validation
- Feature enablement/disablement
- UI updates based on tier
- Usage tracking

#### 2. Watermark System (`client/js/watermark.js`)
- CSS overlay watermarks
- Canvas export watermarks
- Tier-based watermark settings
- Position and styling controls

#### 3. Export Handlers (`client/js/export-handlers.js`)
- JPG export functionality
- html2canvas integration
- Tier-based export quality
- Download management

#### 4. Tier Styles (`client/css/tier-styles.css`)
- Tier-specific styling
- Watermark CSS classes
- Feature visibility controls
- Responsive design

### Server-Side Components

#### 1. Tier Management (`server/tier_management.py`)
- User tier detection
- IP-based usage tracking
- Feature access validation
- Session management

#### 2. Configuration (`config/tiers.json`)
- Shared tier definitions
- Feature mappings
- Usage limits
- Upgrade paths

## Implementation Details

### Tier Detection

#### Client-Side Detection
```javascript
// Initialize tier management
window.tierManagement.initialize();

// Get current tier
const currentTier = window.tierManagement.getCurrentTier();

// Check feature availability
const hasAutoSpacing = window.tierManagement.isFeatureAvailable('autoSpacing');
```

#### Server-Side Detection
```python
from server.tier_management import get_user_tier, track_user_usage

# Detect user tier
tier = get_user_tier(session_id, ip_address, user_token)

# Track usage
track_user_usage(session_id, ip_address, "generate_chart")
```

### Watermark Implementation

#### CSS Overlay Watermark
- Positioned absolutely over chart container
- Tier-based opacity and size
- Bottom-left positioning
- Non-interactive (pointer-events: none)

#### Canvas Export Watermark
- Applied during JPG export process
- Uses html2canvas for capture
- Additional canvas watermark overlay
- Permanent in exported files

### Feature Restrictions

#### Auto-Spacing
- **Noob**: Disabled
- **Registered**: Enabled
- **VIPer**: Enabled

#### Advanced Charts
- **Noob**: Basic charts only
- **Registered**: All chart types
- **VIPer**: All chart types

#### Custom Branding
- **Noob**: Not available
- **Registered**: Not available
- **VIPer**: Available

### Usage Limits

#### Monthly Charts
- **Noob**: 10 charts/month
- **Registered**: 50 charts/month
- **VIPer**: Unlimited

#### File Size Limits
- **Noob**: 5MB
- **Registered**: 10MB
- **VIPer**: 25MB

## Integration Points

### Chart Generation
1. Check tier before generating chart
2. Apply tier-based feature restrictions
3. Track usage for tier enforcement
4. Apply watermark based on tier

### Export Process
1. Validate export permissions
2. Apply tier-based watermark settings
3. Use tier-appropriate export quality
4. Track export usage

### UI Updates
1. Update tier progression bar
2. Show/hide tier-specific elements
3. Display upgrade prompts
4. Apply tier-based styling

## Configuration

### Tier Settings
All tier configurations are stored in `config/tiers.json` and shared between client and server.

### Feature Definitions
Features are defined with:
- **Description**: Human-readable feature description
- **Tiers**: Array of tiers that have access
- **Default Value**: Default setting for the feature

### Usage Limits
Limits are defined per tier with:
- **Monthly Charts**: Maximum charts per month
- **File Size**: Maximum upload file size
- **Concurrent Sessions**: Maximum active sessions

## Testing

### Tier Detection Tests
- Verify correct tier assignment
- Test feature availability
- Validate usage limits
- Check UI updates

### Watermark Tests
- Verify watermark visibility
- Test tier-based settings
- Validate export watermarks
- Check positioning

### Export Tests
- Test JPG export functionality
- Verify watermark inclusion
- Check quality settings
- Validate file naming

## Security Considerations

### Client-Side Security
- Tier detection can be bypassed client-side
- Watermarks can be removed via browser dev tools
- Export restrictions can be circumvented

### Server-Side Validation
- Always validate tier on server
- Track usage server-side
- Enforce limits server-side
- Validate file uploads

### Recommendations
- Implement server-side tier validation
- Use server-side watermarking for exports
- Track usage patterns for abuse detection
- Implement rate limiting

## Future Enhancements

### Planned Features
- Server-side watermark validation
- Advanced usage analytics
- Dynamic tier upgrades
- Payment integration

### Scalability Considerations
- Database storage for usage tracking
- Redis caching for session data
- CDN for static assets
- Load balancing for high traffic

## Troubleshooting

### Common Issues

#### Watermark Not Visible
- Check tier configuration
- Verify CSS positioning
- Ensure z-index is correct
- Check browser compatibility

#### Export Fails
- Verify html2canvas loading
- Check chart container exists
- Validate watermark settings
- Check browser console for errors

#### Tier Detection Issues
- Verify session ID generation
- Check IP address detection
- Validate token format
- Review server logs

### Debug Mode
Enable debug logging by setting:
```javascript
window.tierManagement.debug = true;
```

This will log all tier-related operations to the console.
