# Charting Website Tiered Architecture

## **Tier Overview**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      NOOB       │    │   REGISTERED    │    │      VIPER      │
│   (Anonymous)   │    │     (Free)      │    │   ($3/month)    │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Basic Plotly  │    │ • Enhanced      │    │ • Premium       │
│ • Client-side   │    │ • Hybrid        │    │ • Server-heavy  │
│ • Watermarked   │    │ • Watermarked   │    │ • Branded       │
│ • IP-limited    │    │ • Session-limit │    │ • Unlimited     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## **Architecture Layers**

### **1. Client-Side Layer (All Tiers)**
```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT-SIDE LAYER                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   File      │  │   Chart     │  │   Export    │         │
│  │  Upload     │  │  Rendering  │  │   Tools     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Data      │  │   Basic     │  │   Local     │         │
│  │  Parsing    │  │  Styling    │  │  Storage    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### **2. Server-Side Layer (Tier-Dependent)**
```
┌─────────────────────────────────────────────────────────────┐
│                   SERVER-SIDE LAYER                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   User      │  │   Chart     │  │   Advanced  │         │
│  │  Auth       │  │  Processing │  │  Analytics  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Rate      │  │   Premium   │  │   Custom    │         │
│  │  Limiting   │  │  Features   │  │  Branding   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## **Tier-Specific Architecture**

### **NOOB Tier Architecture**
```
┌─────────────────────────────────────────────────────────────┐
│                        NOOB TIER                            │
├─────────────────────────────────────────────────────────────┤
│  CLIENT-SIDE (100%)                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   File      │  │   Basic     │  │   Watermark │         │
│  │  Upload     │  │  Plotly     │  │   System    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│  SERVER-SIDE (Minimal)                                      │
│  ┌─────────────┐  ┌─────────────┐                          │
│  │   IP        │  │   Rate      │                          │
│  │  Tracking   │  │  Limiting   │                          │
│  └─────────────┘  └─────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

**Server Calls:**
- `POST /api/track-usage` - IP-based usage tracking
- `GET /api/limits` - Check monthly limits
- `POST /api/watermark` - Generate watermarks

### **REGISTERED Tier Architecture**
```
┌─────────────────────────────────────────────────────────────┐
│                    REGISTERED TIER                          │
├─────────────────────────────────────────────────────────────┤
│  CLIENT-SIDE (80%)                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Enhanced  │  │   Advanced  │  │   Session   │         │
│  │   Upload    │  │   Styling   │  │   Storage   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│  SERVER-SIDE (20%)                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   User      │  │   Enhanced  │  │   Code      │         │
│  │   Auth      │  │  Processing │  │  Download   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

**Server Calls:**
- `POST /api/auth/login` - User authentication
- `POST /api/process-enhanced` - Enhanced chart processing
- `GET /api/download-code` - Code generation (limited per session)
- `POST /api/save-preferences` - User preferences

### **VIPER Tier Architecture**
```
┌─────────────────────────────────────────────────────────────┐
│                       VIPER TIER                            │
├─────────────────────────────────────────────────────────────┤
│  CLIENT-SIDE (40%)                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Premium   │  │   Custom    │  │   Advanced  │         │
│  │   Upload    │  │   Branding  │  │   Export    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│  SERVER-SIDE (60%)                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Premium   │  │   Advanced  │  │   Analytics │         │
│  │  Processing │  │  Features   │  │   & Stats   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Custom    │  │   Unlimited │  │   Priority  │         │
│  │  Branding   │  │   Downloads │  │   Support   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

**Server Calls:**
- `POST /api/premium/process` - Premium chart processing
- `POST /api/branding/apply` - Custom branding application
- `GET /api/premium/features` - Advanced chart types
- `POST /api/analytics/track` - Usage analytics
- `GET /api/premium/downloads` - Unlimited downloads

## **Data Flow Architecture**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    USER     │───▶│   CLIENT    │───▶│   SERVER    │
│  INTERFACE  │    │   SIDE      │    │   SIDE      │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Tier      │    │   Local     │    │   Tier-     │
│ Detection   │    │  Processing │    │  Specific   │
└─────────────┘    └─────────────┘    │  Features   │
                                      └─────────────┘
```

## **Security & Code Protection Strategy**

### **Client-Side Protection**
```
┌─────────────────────────────────────────────────────────────┐
│                   CODE PROTECTION                           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Obfuscate │  │   Minify    │  │   Split     │         │
│  │   Critical  │  │   Code      │  │   Logic     │         │
│  │   Functions │  │             │  │   Across    │         │
│  └─────────────┘  └─────────────┘  │   Tiers     │         │
│  ┌─────────────┐  ┌─────────────┐  └─────────────┘         │
│  │   Server    │  │   Dynamic   │  ┌─────────────┐         │
│  │  Validation │  │   Loading   │  │   Watermark │         │
│  │   Required  │  │   of Code   │  │   All Tiers │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### **Server-Side Validation**
```
┌─────────────────────────────────────────────────────────────┐
│                  SERVER VALIDATION                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Tier      │  │   Rate      │  │   Feature   │         │
│  │  Checking   │  │  Limiting   │  │  Access     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   User      │  │   Session   │  │   IP        │         │
│  │  Auth       │  │  Tracking   │  │  Tracking   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## **API Endpoint Architecture**

### **NOOB Endpoints**
```
/api/track-usage     - Track IP-based usage
/api/limits          - Check monthly limits  
/api/watermark       - Generate watermarks
/api/basic-features  - Basic chart features
```

### **REGISTERED Endpoints**
```
/api/auth/*          - Authentication
/api/enhanced/*      - Enhanced features
/api/download/*      - Code downloads (limited)
/api/preferences     - User preferences
```

### **VIPER Endpoints**
```
/api/premium/*       - Premium features
/api/branding/*      - Custom branding
/api/analytics/*     - Usage analytics
/api/unlimited/*     - Unlimited features
```

## **Scalability Considerations**

### **Cost Optimization**
- **NOOB**: Minimal server resources, heavy client-side
- **REGISTERED**: Balanced approach, session-based limits
- **VIPER**: Server-heavy but optimized for cost efficiency

### **Performance Strategy**
- **Caching**: Server-side caching for common operations
- **CDN**: Static assets served via CDN
- **Load Balancing**: Distribute server load across instances
- **Database**: Efficient queries, connection pooling

## **Implementation Roadmap**

### **Phase 1: NOOB Tier**
- Implement IP-based tracking
- Basic client-side functionality
- Watermark system
- Rate limiting

### **Phase 2: REGISTERED Tier**
- User authentication system
- Enhanced features
- Session-based limits
- Code download system

### **Phase 3: VIPER Tier**
- Premium features
- Custom branding
- Analytics system
- Unlimited downloads

## **Technical Requirements**

### **Frontend Technologies**
- HTML5, CSS3, JavaScript (ES6+)
- Plotly.js for charting
- Local storage for session management
- Canvas API for watermarking

### **Backend Technologies**
- Python Flask/Django or Node.js
- PostgreSQL/MongoDB for data storage
- Redis for caching and session management
- AWS/GCP for cloud hosting

### **Security Measures**
- JWT tokens for authentication
- Rate limiting middleware
- Input validation and sanitization
- HTTPS encryption
- CORS configuration

This architecture provides a robust, scalable foundation that protects code while delivering appropriate functionality for each tier level.
