# 📊 System Architecture & Flow Diagrams

This document contains interactive flowcharts and diagrams explaining the WhatsApp Friendship Analyzer architecture.

## 🏗️ High-Level Architecture

```mermaid
graph TB
    A[WhatsApp Chat Export<br/>.txt file] --> B[Parser Layer]
    B --> C[Data Enrichment]
    C --> D[Analysis Engine]
    D --> E[Classification System]
    E --> F[Report Generation]
    
    B --> B1[Regex Pattern Matching]
    B --> B2[Multi-Format Support]
    B --> B3[System Message Filter]
    
    C --> C1[Sentiment Analysis<br/>TextBlob]
    C --> C2[Emoji Extraction]
    C --> C3[Time Analysis]
    
    D --> D1[Tone Detection]
    D --> D2[Pattern Recognition]
    D --> D3[Behavioral Analysis]
    
    E --> E1[21+ Indicators]
    E --> E2[Weighted Scoring]
    E --> E3[12 Relationship Types]
    
    F --> F1[HTML Full Report]
    F --> F2[HTML Compact Card]
    F --> F3[PNG Image 1080x1350]
    
    style A fill:#667eea,stroke:#333,color:#fff
    style B fill:#764ba2,stroke:#333,color:#fff
    style C fill:#f093fb,stroke:#333,color:#fff
    style D fill:#4facfe,stroke:#333,color:#fff
    style E fill:#43e97b,stroke:#333,color:#fff
    style F fill:#fa709a,stroke:#333,color:#fff
```

## 🔄 Data Processing Flow

```mermaid
flowchart TD
    Start([Start: Chat Export]) --> Read[Read File Line by Line]
    Read --> TryParse{Try Regex<br/>Patterns}
    
    TryParse -->|Pattern 1| P1[Bracketed AM/PM<br/>[MM/DD/YY HH:MM:SS AM]]
    TryParse -->|Pattern 2| P2[US Format<br/>MM/DD/YY HH:MM - ]
    TryParse -->|Pattern 3| P3[EU Format<br/>DD/MM/YY HH:MM - ]
    TryParse -->|Pattern 4| P4[Bracketed<br/>[DD/MM/YY HH:MM:SS]]
    
    P1 --> Parse[Extract Components]
    P2 --> Parse
    P3 --> Parse
    P4 --> Parse
    TryParse -->|No Match| Append[Append to<br/>Previous Message]
    
    Parse --> System{System<br/>Message?}
    System -->|Yes| FilterSys[Mark as System<br/>Sender = 'System']
    System -->|No| FilterUser[User Message]
    
    FilterSys --> Store[Store Message]
    FilterUser --> Store
    Append --> Store
    
    Store --> More{More<br/>Lines?}
    More -->|Yes| Read
    More -->|No| Enrich[Enrich Messages]
    
    Enrich --> Sentiment[Add Sentiment Scores]
    Sentiment --> Emoji[Extract Emojis]
    Emoji --> Time[Calculate Response Times]
    Time --> TOD[Mark Time of Day]
    TOD --> Analyze[Analyze Patterns]
    
    Analyze --> Classify[Classify Relationship]
    Classify --> Generate[Generate Reports]
    Generate --> End([End: 3 Output Files])
    
    style Start fill:#667eea,stroke:#333,color:#fff
    style End fill:#43e97b,stroke:#333,color:#fff
    style Parse fill:#4facfe,stroke:#333,color:#fff
    style Classify fill:#fa709a,stroke:#333,color:#fff
```

## 🎯 Relationship Classification Algorithm

```mermaid
flowchart TD
    Start([Input: Parsed Messages]) --> Init[Initialize 12 Scores to 0]
    
    Init --> I1[Indicator 1:<br/>Message Frequency]
    I1 --> Freq{Msgs/Day?}
    Freq -->|>100| F1[Romantic +30<br/>Close Friends +20]
    Freq -->|50-100| F2[Romantic +20<br/>Close Friends +25]
    Freq -->|20-50| F3[Close Friends +20<br/>Casual +15]
    Freq -->|5-20| F4[Casual +20<br/>Colleagues +15]
    Freq -->|<5| F5[Acquaintances +20]
    
    F1 --> I2[Indicator 2:<br/>Duration]
    F2 --> I2
    F3 --> I2
    F4 --> I2
    F5 --> I2
    
    I2 --> Dur{Duration?}
    Dur -->|<30 days<br/>& high freq| D1[Romantic +20]
    Dur -->|>365 days| D2[Close Friends +15<br/>Siblings +10]
    Dur -->|Otherwise| D3[No change]
    
    D1 --> I3[Indicator 3:<br/>Tone Analysis]
    D2 --> I3
    D3 --> I3
    
    I3 --> Tone{Tone?}
    Tone -->|Casual >25%| T1[Close Friends +25<br/>Romantic -10]
    Tone -->|Formal >15%| T2[Colleagues +25<br/>Professional +20]
    Tone -->|Playful >2%| T3[Close Friends +15]
    
    T1 --> I4[Indicator 4:<br/>Content Analysis]
    T2 --> I4
    T3 --> I4
    
    I4 --> Content{Content?}
    Content -->|Life Planning >1%| C1[Romantic +30<br/>Established +25]
    Content -->|Shared Parents >2%| C2[Siblings +40<br/>Romantic -30]
    Content -->|Work Terms >20| C3[Colleagues +20]
    
    C1 --> I5[Indicator 5:<br/>Group Detection]
    C2 --> I5
    C3 --> I5
    
    I5 --> Group{Participants?}
    Group -->|>2 people| G1[Close Friends +30<br/>Romantic -50]
    Group -->|2 people| G2[Romantic +10<br/>Close Friends +10]
    
    G1 --> More[Continue with<br/>16 more indicators...]
    G2 --> More
    
    More --> Final[All 21 Indicators<br/>Processed]
    Final --> Max[Find Max Score]
    Max --> Conf{Score Value?}
    
    Conf -->|>120| Conf1[Confidence:<br/>VERY HIGH]
    Conf -->|80-120| Conf2[Confidence:<br/>HIGH]
    Conf -->|50-80| Conf3[Confidence:<br/>MODERATE]
    Conf -->|<50| Conf4[Confidence:<br/>LOW]
    
    Conf1 --> Output[Output:<br/>Relationship Type<br/>+ Confidence]
    Conf2 --> Output
    Conf3 --> Output
    Conf4 --> Output
    
    Output --> End([End: Classification])
    
    style Start fill:#667eea,stroke:#333,color:#fff
    style End fill:#43e97b,stroke:#333,color:#fff
    style Max fill:#fa709a,stroke:#333,color:#fff
    style Output fill:#f093fb,stroke:#333,color:#fff
```

## 🧠 Sentiment Analysis Pipeline

```mermaid
flowchart LR
    A[Message Text] --> B[TextBlob<br/>Processing]
    B --> C[Extract<br/>Polarity]
    B --> D[Extract<br/>Subjectivity]
    
    C --> E{Polarity<br/>Score}
    E -->|> 0.5| E1[Very Positive<br/>😄]
    E -->|0.1 to 0.5| E2[Positive<br/>🙂]
    E -->|-0.1 to 0.1| E3[Neutral<br/>😐]
    E -->|-0.5 to -0.1| E4[Negative<br/>🙁]
    E -->|< -0.5| E5[Very Negative<br/>😢]
    
    D --> F{Subjectivity}
    F -->|> 0.7| F1[Very Subjective<br/>Opinion-based]
    F -->|0.3 to 0.7| F2[Balanced]
    F -->|< 0.3| F3[Objective<br/>Fact-based]
    
    E1 --> G[Aggregate<br/>Statistics]
    E2 --> G
    E3 --> G
    E4 --> G
    E5 --> G
    F1 --> G
    F2 --> G
    F3 --> G
    
    G --> H[Average<br/>Sentiment]
    G --> I[Sentiment<br/>Trend]
    
    H --> J[Per-Person<br/>Profile]
    I --> J
    
    J --> K([Output:<br/>Sentiment Metrics])
    
    style A fill:#667eea,stroke:#333,color:#fff
    style B fill:#4facfe,stroke:#333,color:#fff
    style K fill:#43e97b,stroke:#333,color:#fff
```

## 📈 Report Generation Process

```mermaid
flowchart TD
    A[Analysis Results] --> B{Generate<br/>Reports}
    
    B --> C[HTML Full Report]
    B --> D[HTML Compact Card]
    B --> E[PNG Image]
    
    C --> C1[Header Section]
    C1 --> C2[Overview Stats]
    C2 --> C3[Relationship<br/>Classification]
    C3 --> C4[Communication<br/>Analysis]
    C4 --> C5[Message<br/>Distribution]
    C5 --> C6[Personality<br/>Profiles]
    C6 --> C7[Behavioral<br/>Indicators]
    C7 --> C8[Final Judgment]
    C8 --> C9[Key Takeaways]
    C9 --> C10[Save HTML]
    
    D --> D1[Card Header]
    D1 --> D2[4 Stat Boxes]
    D2 --> D3[Top 3 Insights]
    D3 --> D4[Top 3 Scores]
    D4 --> D5[Footer]
    D5 --> D6[Save HTML<br/>Print-Ready]
    
    E --> E1[Create Canvas<br/>1080x1350]
    E1 --> E2[Gradient<br/>Background]
    E2 --> E3[Relationship<br/>Type + Emoji]
    E3 --> E4[Key Stats]
    E4 --> E5[Insights]
    E5 --> E6[Score Bars]
    E6 --> E7[Save PNG]
    
    C10 --> F[data/analysis/<br/>report_*.html]
    D6 --> G[data/analysis/<br/>card_*.html]
    E7 --> H[data/analysis/<br/>image_*.png]
    
    F --> I([3 Output Files<br/>Ready!])
    G --> I
    H --> I
    
    style A fill:#667eea,stroke:#333,color:#fff
    style I fill:#43e97b,stroke:#333,color:#fff
    style C fill:#fa709a,stroke:#333,color:#fff
    style D fill:#f093fb,stroke:#333,color:#fff
    style E fill:#4facfe,stroke:#333,color:#fff
```

## 🔍 Tone Detection System

```mermaid
flowchart TD
    Start[Message Collection] --> Scan[Scan Messages]
    
    Scan --> Cat1[Category 1:<br/>Casual/Slang]
    Scan --> Cat2[Category 2:<br/>Formal]
    Scan --> Cat3[Category 3:<br/>Playful]
    Scan --> Cat4[Category 4:<br/>Insults]
    Scan --> Cat5[Category 5:<br/>Roasting]
    
    Cat1 --> K1{Keywords:<br/>bro, dude, lol,<br/>lmao, yeet, lit}
    Cat2 --> K2{Keywords:<br/>please, thank you,<br/>sir, madam}
    Cat3 --> K3{Keywords:<br/>playful teasing,<br/>jokes}
    Cat4 --> K4{Keywords:<br/>shut up, stfu,<br/>ur dumb}
    Cat5 --> K5{Keywords:<br/>loser, dummy,<br/>nerd, weirdo}
    
    K1 --> C1[Count<br/>Occurrences]
    K2 --> C2[Count<br/>Occurrences]
    K3 --> C3[Count<br/>Occurrences]
    K4 --> C4[Count<br/>Occurrences]
    K5 --> C5[Count<br/>Occurrences]
    
    C1 --> P1[Calculate<br/>Percentage]
    C2 --> P2[Calculate<br/>Percentage]
    C3 --> P3[Calculate<br/>Percentage]
    C4 --> P4[Calculate<br/>Percentage]
    C5 --> P5[Calculate<br/>Percentage]
    
    P1 --> Interp{Interpret}
    P2 --> Interp
    P3 --> Interp
    P4 --> Interp
    P5 --> Interp
    
    Interp -->|Casual >25%| I1[Close Friends<br/>Likely]
    Interp -->|Formal >15%| I2[Professional<br/>Likely]
    Interp -->|Roasting >2%| I3[Close Friends<br/>Who Tease]
    Interp -->|Insults >5%| I4[Conflict<br/>Relationship]
    
    I1 --> Output[Tone Profile]
    I2 --> Output
    I3 --> Output
    I4 --> Output
    
    Output --> End([Use in<br/>Classification])
    
    style Start fill:#667eea,stroke:#333,color:#fff
    style End fill:#43e97b,stroke:#333,color:#fff
    style Output fill:#fa709a,stroke:#333,color:#fff
```

## 🎭 Personality Profiling

```mermaid
flowchart LR
    A[User Messages] --> B[Extract Features]
    
    B --> F1[Message Count]
    B --> F2[Avg Message<br/>Length]
    B --> F3[Emoji Usage]
    B --> F4[Sentiment Avg]
    B --> F5[Night Owl %]
    B --> F6[Initiator Count]
    B --> F7[Response Time]
    
    F1 --> C{Classify<br/>Style}
    F2 --> C
    F3 --> C
    
    C -->|Msg Length >100| S1[Expressive<br/>📝]
    C -->|Emoji >50| S2[Emotive<br/>😊]
    C -->|Msg Count High| S3[Talkative<br/>💬]
    C -->|Otherwise| S4[Reserved<br/>🤐]
    
    F4 --> E{Emotional<br/>Tone}
    E -->|Positive| E1[Optimistic<br/>😄]
    E -->|Neutral| E2[Balanced<br/>😐]
    E -->|Negative| E3[Pessimistic<br/>😔]
    
    F5 --> N{Night<br/>Activity}
    N -->|>30%| N1[Night Owl<br/>🦉]
    N -->|Otherwise| N2[Day Person<br/>☀️]
    
    F6 --> I{Initiation}
    I -->|>60%| I1[Leader<br/>👑]
    I -->|40-60%| I2[Balanced<br/>⚖️]
    I -->|<40%| I3[Follower<br/>👥]
    
    F7 --> R{Response<br/>Speed}
    R -->|<5 min| R1[Very Engaged<br/>⚡]
    R -->|5-30 min| R2[Active<br/>✓]
    R -->|>30 min| R3[Casual<br/>⏰]
    
    S1 --> Profile[Complete<br/>Personality Profile]
    S2 --> Profile
    S3 --> Profile
    S4 --> Profile
    E1 --> Profile
    E2 --> Profile
    E3 --> Profile
    N1 --> Profile
    N2 --> Profile
    I1 --> Profile
    I2 --> Profile
    I3 --> Profile
    R1 --> Profile
    R2 --> Profile
    R3 --> Profile
    
    Profile --> Output([Display in<br/>Report])
    
    style A fill:#667eea,stroke:#333,color:#fff
    style Profile fill:#fa709a,stroke:#333,color:#fff
    style Output fill:#43e97b,stroke:#333,color:#fff
```

## 🔢 Scoring Matrix Visualization

```mermaid
graph TD
    subgraph "Message Frequency Scoring"
        A1[">100 msgs/day"] --> B1[Romantic Dating +30]
        A1 --> B2[Close Friends +20]
        A2["50-100 msgs/day"] --> B3[Romantic Dating +20]
        A2 --> B4[Close Friends +25]
        A3["20-50 msgs/day"] --> B5[Close Friends +20]
        A3 --> B6[Casual Friends +15]
        A4["5-20 msgs/day"] --> B7[Casual Friends +20]
        A4 --> B8[Colleagues +15]
        A5["<5 msgs/day"] --> B9[Acquaintances +20]
    end
    
    subgraph "Tone Modifiers"
        C1["Casual >25%"] --> D1[Close Friends +25]
        C1 --> D2[Romantic -10]
        C2["Formal >15%"] --> D3[Colleagues +25]
        C2 --> D4[Professional +20]
        C3["Roasting >2%"] --> D5[Close Friends +20]
        C3 --> D6[Romantic -15]
    end
    
    subgraph "Content Boosters"
        E1["Life Planning >1%"] --> F1[Romantic Dating +30]
        E1 --> F2[Romantic Established +25]
        E2["Shared Parents >2%"] --> F3[Siblings +40]
        E2 --> F4[Romantic -30]
        E3["Work Terms >20"] --> F5[Colleagues +20]
        E3 --> F6[Professional +15]
    end
    
    subgraph "Group Override"
        G1["Participants >2"] --> H1[Close Friends +30]
        G1 --> H2[Romantic -50]
        G1 --> H3[Romantic Established -50]
    end
    
    B1 --> Final
    B2 --> Final
    B3 --> Final
    B4 --> Final
    B5 --> Final
    B6 --> Final
    B7 --> Final
    B8 --> Final
    B9 --> Final
    D1 --> Final
    D2 --> Final
    D3 --> Final
    D4 --> Final
    D5 --> Final
    D6 --> Final
    F1 --> Final
    F2 --> Final
    F3 --> Final
    F4 --> Final
    F5 --> Final
    F6 --> Final
    H1 --> Final
    H2 --> Final
    H3 --> Final
    
    Final[Sum All Scores]
    Final --> Result[Select Max Score<br/>= Relationship Type]
    
    style A1 fill:#667eea,stroke:#333,color:#fff
    style Final fill:#fa709a,stroke:#333,color:#fff
    style Result fill:#43e97b,stroke:#333,color:#fff
```

## 🌐 System Component Interaction

```mermaid
sequenceDiagram
    participant U as User
    participant M as Main Script
    participant P as Parser
    participant A as Analyzer
    participant C as Classifier
    participant R as Report Generator
    participant F as File System
    
    U->>M: Run process_all_chats.py
    M->>F: List files in data/raw/
    F-->>M: Return .txt files
    
    loop For each chat file
        M->>P: Parse chat file
        P->>P: Apply regex patterns
        P->>P: Filter system messages
        P->>P: Extract participants
        P-->>M: Return parsed messages
        
        M->>A: Analyze messages
        A->>A: Calculate sentiment
        A->>A: Extract emojis
        A->>A: Detect tone
        A->>A: Find patterns
        A-->>M: Return analysis data
        
        M->>C: Classify relationship
        C->>C: Score 21+ indicators
        C->>C: Calculate confidence
        C-->>M: Return classification
        
        M->>R: Generate reports
        R->>R: Create HTML full
        R->>R: Create HTML card
        R->>R: Create PNG image
        R->>F: Save 3 files
        F-->>R: Files saved
        R-->>M: Generation complete
    end
    
    M-->>U: All reports generated ✓
    
    Note over U,F: Process completes in ~2-7 seconds per chat
```

---

## 📱 Mobile-Friendly Views

All diagrams above are interactive and responsive. Click/tap on any node for more details (in supported viewers like GitHub, GitLab, or Mermaid Live Editor).

## 🎨 Color Legend

- 🟣 **Purple (#667eea)**: Input/Start points
- 🟢 **Green (#43e97b)**: Output/End points  
- 🔴 **Pink (#fa709a)**: Critical decision points
- 🔵 **Blue (#4facfe)**: Processing steps
- 🟡 **Pink-Purple (#f093fb)**: Data transformations

---

**View these diagrams interactively on GitHub Pages!**
