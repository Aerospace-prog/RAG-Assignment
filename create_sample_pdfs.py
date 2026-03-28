#!/usr/bin/env python3
"""
Create sample PDFs for testing the RAG system.
Generates PDFs with different content types to demonstrate versatility.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

# Create fixtures directory if it doesn't exist
FIXTURES_DIR = "backend/tests/fixtures"
os.makedirs(FIXTURES_DIR, exist_ok=True)


def create_business_report():
    """Create a sample business report PDF."""
    filename = os.path.join(FIXTURES_DIR, "business_report.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='darkblue',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    story.append(Paragraph("Q4 2024 Business Performance Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    exec_summary = """
    This report provides a comprehensive analysis of our company's performance in Q4 2024.
    Revenue increased by 23% year-over-year, reaching $4.2 million. Customer acquisition
    costs decreased by 15% while retention rates improved to 94%. Our new product line
    contributed 18% of total revenue, exceeding initial projections by 12%.
    """
    story.append(Paragraph(exec_summary, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Financial Performance
    story.append(Paragraph("Financial Performance", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    financial = """
    Total revenue for Q4 2024 was $4.2 million, representing a 23% increase compared to
    Q4 2023. Gross profit margin improved from 62% to 68%, driven by operational
    efficiencies and economies of scale. Operating expenses were well-controlled at
    $1.8 million, resulting in an EBITDA of $1.1 million. Net profit reached $850,000,
    a 45% improvement over the previous year.
    """
    story.append(Paragraph(financial, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Customer Metrics
    story.append(Paragraph("Customer Metrics", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    customers = """
    We acquired 1,250 new customers in Q4, bringing our total customer base to 8,400.
    Customer retention rate improved to 94%, up from 89% in Q3. Average customer lifetime
    value increased to $12,500, while customer acquisition cost decreased to $850.
    Net Promoter Score (NPS) reached 72, indicating strong customer satisfaction.
    """
    story.append(Paragraph(customers, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Product Development
    story.append(Paragraph("Product Development", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    product = """
    Our new AI-powered analytics platform launched in October exceeded expectations,
    generating $750,000 in revenue within the first two months. The platform has been
    adopted by 320 customers with an average contract value of $2,340. User engagement
    metrics show daily active usage of 78%, significantly higher than industry benchmarks.
    """
    story.append(Paragraph(product, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Market Analysis
    story.append(Paragraph("Market Analysis", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    market = """
    The overall market for our solutions grew by 18% in 2024, reaching $2.3 billion.
    Our market share increased from 3.2% to 4.1%, positioning us as the fifth-largest
    player in the space. Key competitors include TechCorp (22% market share), DataSys
    (15%), and AnalyticsPro (12%). Our differentiation through AI capabilities and
    superior customer service continues to drive growth.
    """
    story.append(Paragraph(market, styles['BodyText']))
    story.append(PageBreak())
    
    # Challenges and Risks
    story.append(Paragraph("Challenges and Risks", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    challenges = """
    Despite strong performance, we face several challenges. Increased competition from
    well-funded startups may pressure pricing. Talent acquisition remains difficult in
    key technical roles, with average time-to-hire at 87 days. Supply chain disruptions
    could impact our hardware component availability. Regulatory changes in data privacy
    may require significant compliance investments.
    """
    story.append(Paragraph(challenges, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # 2025 Outlook
    story.append(Paragraph("2025 Outlook", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    outlook = """
    We project 30% revenue growth in 2025, targeting $22 million in annual revenue.
    Key initiatives include expanding into European markets, launching two new product
    features, and growing the team from 85 to 120 employees. We plan to raise a Series B
    round of $15 million to fund this expansion. Customer acquisition targets are set at
    6,000 new customers with a retention rate goal of 95%.
    """
    story.append(Paragraph(outlook, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Conclusion
    story.append(Paragraph("Conclusion", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    conclusion = """
    Q4 2024 demonstrated strong execution across all key metrics. The team delivered
    exceptional results while maintaining operational discipline. As we enter 2025,
    we are well-positioned to capitalize on market opportunities and continue our
    growth trajectory. Our focus remains on customer success, product innovation,
    and sustainable scaling.
    """
    story.append(Paragraph(conclusion, styles['BodyText']))
    
    doc.build(story)
    print(f"✅ Created: {filename}")


def create_research_paper():
    """Create a sample research paper PDF."""
    filename = os.path.join(FIXTURES_DIR, "research_paper.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor='darkblue',
        spaceAfter=20,
        alignment=TA_CENTER
    )
    story.append(Paragraph("The Impact of Machine Learning on Healthcare Diagnostics", title_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Authors
    author_style = ParagraphStyle(
        'Authors',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    story.append(Paragraph("Dr. Sarah Johnson, Dr. Michael Chen, Dr. Emily Rodriguez", author_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Abstract
    story.append(Paragraph("Abstract", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    abstract = """
    Machine learning algorithms have revolutionized medical diagnostics over the past decade.
    This paper examines the application of deep learning models in detecting various diseases
    from medical imaging. We analyze 15 major studies involving over 500,000 patients and
    demonstrate that ML-based diagnostic systems achieve accuracy rates of 92-97%, comparable
    to or exceeding human expert performance. Key findings include improved early detection
    of cancers, reduced false positive rates, and significant time savings in diagnostic
    workflows. We discuss implementation challenges, ethical considerations, and future
    research directions.
    """
    story.append(Paragraph(abstract, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Introduction
    story.append(Paragraph("1. Introduction", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    intro = """
    Healthcare diagnostics have traditionally relied on human expertise and manual analysis
    of medical data. However, the exponential growth in medical imaging data and the
    complexity of modern diagnostic criteria have created opportunities for computational
    approaches. Machine learning, particularly deep learning using convolutional neural
    networks (CNNs), has emerged as a powerful tool for automated medical image analysis.
    This technology promises to improve diagnostic accuracy, reduce costs, and increase
    access to quality healthcare globally.
    """
    story.append(Paragraph(intro, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Methodology
    story.append(Paragraph("2. Methodology", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    methodology = """
    We conducted a systematic review of peer-reviewed studies published between 2019 and 2024
    that evaluated machine learning applications in medical diagnostics. Our search covered
    PubMed, IEEE Xplore, and Google Scholar databases. Inclusion criteria required studies
    with at least 1,000 patient samples, validated ML models, and comparison with human
    expert performance. We extracted data on accuracy, sensitivity, specificity, and
    implementation details. Statistical meta-analysis was performed using random-effects
    models to account for study heterogeneity.
    """
    story.append(Paragraph(methodology, styles['BodyText']))
    story.append(PageBreak())
    
    # Results
    story.append(Paragraph("3. Results", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    results = """
    Our analysis included 15 high-quality studies encompassing 523,000 patients across
    multiple diagnostic domains. In radiology, ML models achieved 94.2% accuracy in
    detecting lung cancer from CT scans, compared to 91.8% for radiologists. For diabetic
    retinopathy screening, automated systems reached 96.1% sensitivity and 93.4% specificity.
    In dermatology, skin cancer detection models demonstrated 95.3% accuracy, matching
    dermatologist performance. Processing time was reduced by an average of 73%, from
    15 minutes per case to 4 minutes.
    """
    story.append(Paragraph(results, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Discussion
    story.append(Paragraph("4. Discussion", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    discussion = """
    The evidence strongly supports the clinical utility of ML-based diagnostic systems.
    These tools excel at pattern recognition tasks and can process large volumes of data
    consistently. However, several challenges remain. Model interpretability is crucial
    for clinical adoption, as physicians need to understand diagnostic reasoning. Data
    quality and bias in training datasets can lead to performance disparities across
    demographic groups. Integration with existing healthcare IT systems requires
    significant technical and organizational effort. Regulatory frameworks are still
    evolving to address AI-based medical devices.
    """
    story.append(Paragraph(discussion, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Conclusion
    story.append(Paragraph("5. Conclusion", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    conclusion = """
    Machine learning has demonstrated remarkable potential in healthcare diagnostics,
    achieving expert-level performance across multiple domains. As technology matures
    and regulatory frameworks develop, we anticipate widespread clinical adoption.
    Future research should focus on improving model interpretability, addressing bias,
    and conducting large-scale prospective trials. The combination of human expertise
    and AI capabilities promises to enhance diagnostic accuracy and expand access to
    quality healthcare worldwide.
    """
    story.append(Paragraph(conclusion, styles['BodyText']))
    
    doc.build(story)
    print(f"✅ Created: {filename}")


def create_technical_manual():
    """Create a sample technical manual PDF."""
    filename = os.path.join(FIXTURES_DIR, "technical_manual.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor='darkblue',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    story.append(Paragraph("CloudSync Pro - Technical Documentation", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Overview
    story.append(Paragraph("System Overview", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    overview = """
    CloudSync Pro is an enterprise-grade file synchronization and backup solution designed
    for distributed teams. The system provides real-time file synchronization across
    multiple devices, automated backup scheduling, version control, and end-to-end encryption.
    It supports Windows, macOS, Linux, iOS, and Android platforms. The architecture uses
    a hybrid cloud-edge model for optimal performance and reliability.
    """
    story.append(Paragraph(overview, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # System Requirements
    story.append(Paragraph("System Requirements", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    requirements = """
    Minimum requirements: 4GB RAM, 2GHz dual-core processor, 10GB available storage,
    broadband internet connection (5 Mbps minimum). Recommended: 8GB RAM, 3GHz quad-core
    processor, 50GB SSD storage, 25 Mbps internet connection. Operating systems: Windows 10
    or later, macOS 11 or later, Ubuntu 20.04 or later. Mobile: iOS 14+ or Android 10+.
    Network: Port 443 (HTTPS) must be open for cloud communication.
    """
    story.append(Paragraph(requirements, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Installation
    story.append(Paragraph("Installation Guide", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    installation = """
    Download the installer from cloudsyncpro.com/download. Run the installer with
    administrator privileges. Accept the license agreement and choose installation
    directory. The default location is C:\\Program Files\\CloudSync Pro on Windows
    or /Applications on macOS. During installation, you will be prompted to create
    or sign in to your CloudSync account. After installation, the application will
    launch automatically and begin initial configuration.
    """
    story.append(Paragraph(installation, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Configuration
    story.append(Paragraph("Configuration", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    configuration = """
    Open CloudSync Pro and navigate to Settings. Under Sync Folders, click Add Folder
    to select directories for synchronization. Configure sync frequency: Real-time,
    Every 15 minutes, Hourly, or Daily. Set bandwidth limits under Network Settings
    to control upload/download speeds. Enable encryption in Security Settings and
    choose between AES-256 or ChaCha20-Poly1305. Configure backup retention policy:
    Keep all versions, Keep last 30 days, or Custom retention rules.
    """
    story.append(Paragraph(configuration, styles['BodyText']))
    story.append(PageBreak())
    
    # Features
    story.append(Paragraph("Key Features", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    features = """
    Real-time Synchronization: Files are synced automatically within seconds of changes.
    Version Control: Access up to 100 previous versions of any file. Conflict Resolution:
    Automatic detection and resolution of conflicting changes. Selective Sync: Choose
    which folders to sync on each device. Offline Access: Work with files offline; changes
    sync when connection is restored. Sharing: Generate secure links for file sharing with
    expiration dates and password protection. Team Collaboration: Real-time collaboration
    with file locking and change notifications.
    """
    story.append(Paragraph(features, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Troubleshooting
    story.append(Paragraph("Troubleshooting", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    troubleshooting = """
    Sync not working: Check internet connection and verify CloudSync service status at
    status.cloudsyncpro.com. Ensure sufficient storage space is available. Check firewall
    settings allow CloudSync Pro. Files not appearing: Force sync by right-clicking the
    system tray icon and selecting Sync Now. Verify folder is included in sync settings.
    Check file isn't excluded by sync rules. Slow performance: Reduce sync frequency or
    enable bandwidth throttling. Pause sync during high-priority tasks. Consider upgrading
    internet connection or hardware.
    """
    story.append(Paragraph(troubleshooting, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # API Documentation
    story.append(Paragraph("API Documentation", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    api = """
    CloudSync Pro provides a RESTful API for programmatic access. Base URL:
    https://api.cloudsyncpro.com/v1. Authentication uses OAuth 2.0 with bearer tokens.
    Key endpoints: GET /files - List files, POST /files - Upload file, GET /files/{id} -
    Download file, DELETE /files/{id} - Delete file, GET /versions/{id} - List versions,
    POST /share - Create share link. Rate limits: 1000 requests per hour for standard
    accounts, 10000 for enterprise. Full API reference available at
    docs.cloudsyncpro.com/api.
    """
    story.append(Paragraph(api, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Support
    story.append(Paragraph("Support and Resources", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    support = """
    For technical support, visit support.cloudsyncpro.com or email support@cloudsyncpro.com.
    Enterprise customers have access to 24/7 phone support at 1-800-CLOUDSYNC. Knowledge
    base with tutorials and FAQs available at help.cloudsyncpro.com. Community forum at
    community.cloudsyncpro.com for peer support. Video tutorials on YouTube channel
    @CloudSyncPro. System status and maintenance notifications at status.cloudsyncpro.com.
    """
    story.append(Paragraph(support, styles['BodyText']))
    
    doc.build(story)
    print(f"✅ Created: {filename}")


def create_recipe_book():
    """Create a sample recipe book PDF."""
    filename = os.path.join(FIXTURES_DIR, "recipe_book.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='darkgreen',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    story.append(Paragraph("Healthy Mediterranean Recipes", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Recipe 1
    story.append(Paragraph("Greek Lemon Chicken with Roasted Vegetables", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    recipe1_intro = """
    This classic Mediterranean dish combines tender chicken with aromatic herbs and fresh
    lemon. The roasted vegetables add color, nutrition, and complementary flavors. Perfect
    for a healthy weeknight dinner that's ready in 45 minutes. Serves 4 people.
    """
    story.append(Paragraph(recipe1_intro, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Ingredients:", styles['Heading3']))
    ingredients1 = """
    4 chicken breasts (6 oz each), 3 tablespoons olive oil, 2 lemons (juiced and zested),
    4 garlic cloves (minced), 2 teaspoons dried oregano, 1 teaspoon dried thyme, Salt and
    black pepper to taste, 2 red bell peppers (cut into chunks), 2 zucchini (sliced),
    1 red onion (cut into wedges), 1 cup cherry tomatoes, Fresh parsley for garnish.
    """
    story.append(Paragraph(ingredients1, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Instructions:", styles['Heading3']))
    instructions1 = """
    Preheat oven to 400°F (200°C). In a bowl, mix olive oil, lemon juice, lemon zest,
    garlic, oregano, thyme, salt, and pepper. Place chicken breasts in a baking dish and
    pour half the marinade over them. Arrange vegetables around the chicken and drizzle
    with remaining marinade. Roast for 35-40 minutes until chicken reaches 165°F internal
    temperature. Let rest 5 minutes before serving. Garnish with fresh parsley and serve
    with crusty bread or rice.
    """
    story.append(Paragraph(instructions1, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Recipe 2
    story.append(Paragraph("Mediterranean Quinoa Salad", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    recipe2_intro = """
    A refreshing and nutritious salad packed with protein, fiber, and Mediterranean flavors.
    This versatile dish works as a main course or side dish and keeps well in the
    refrigerator for up to 3 days. Preparation time: 25 minutes. Serves 6 people.
    """
    story.append(Paragraph(recipe2_intro, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Ingredients:", styles['Heading3']))
    ingredients2 = """
    2 cups quinoa (uncooked), 4 cups vegetable broth, 1 cucumber (diced), 2 cups cherry
    tomatoes (halved), 1 red onion (finely chopped), 1 cup Kalamata olives (pitted and
    halved), 1 cup feta cheese (crumbled), 1/4 cup fresh mint (chopped), 1/4 cup fresh
    parsley (chopped), 1/3 cup olive oil, 3 tablespoons lemon juice, 2 garlic cloves
    (minced), 1 teaspoon dried oregano, Salt and pepper to taste.
    """
    story.append(Paragraph(ingredients2, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Instructions:", styles['Heading3']))
    instructions2 = """
    Rinse quinoa thoroughly under cold water. In a pot, bring vegetable broth to a boil,
    add quinoa, reduce heat, cover, and simmer for 15 minutes until liquid is absorbed.
    Fluff with a fork and let cool to room temperature. In a large bowl, combine cooled
    quinoa, cucumber, tomatoes, onion, olives, feta, mint, and parsley. In a small bowl,
    whisk together olive oil, lemon juice, garlic, oregano, salt, and pepper. Pour dressing
    over salad and toss gently. Refrigerate for at least 30 minutes before serving to allow
    flavors to meld.
    """
    story.append(Paragraph(instructions2, styles['BodyText']))
    story.append(PageBreak())
    
    # Recipe 3
    story.append(Paragraph("Spanish Seafood Paella", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    recipe3_intro = """
    An authentic Spanish rice dish featuring a medley of seafood, saffron, and aromatic
    spices. This impressive one-pan meal is perfect for entertaining guests. While it
    requires attention, the result is worth the effort. Cooking time: 50 minutes. Serves 6.
    """
    story.append(Paragraph(recipe3_intro, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Ingredients:", styles['Heading3']))
    ingredients3 = """
    3 cups short-grain rice (Bomba or Arborio), 6 cups seafood stock, 1/2 teaspoon saffron
    threads, 1/4 cup olive oil, 1 onion (diced), 4 garlic cloves (minced), 1 red bell
    pepper (sliced), 1 can (14 oz) diced tomatoes, 1 teaspoon smoked paprika, 12 large
    shrimp (peeled and deveined), 12 mussels (cleaned), 8 oz squid (cut into rings),
    1 cup frozen peas, 1 lemon (cut into wedges), Fresh parsley for garnish, Salt to taste.
    """
    story.append(Paragraph(ingredients3, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Instructions:", styles['Heading3']))
    instructions3 = """
    Warm seafood stock and steep saffron threads in it. In a large paella pan or wide
    skillet, heat olive oil over medium heat. Sauté onion until soft, add garlic and bell
    pepper, cook 3 minutes. Add tomatoes and paprika, cook 5 minutes. Spread rice evenly
    in pan, pour in saffron stock, and bring to a boil. Reduce heat and simmer without
    stirring for 15 minutes. Arrange shrimp, mussels, and squid on top, scatter peas over
    rice. Cover and cook 10 minutes until seafood is cooked and rice is tender. Remove from
    heat, cover with foil, and rest 5 minutes. Garnish with parsley and lemon wedges.
    """
    story.append(Paragraph(instructions3, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Nutritional Info
    story.append(Paragraph("Nutritional Information", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    nutrition = """
    Greek Lemon Chicken: 380 calories per serving, 32g protein, 18g carbohydrates, 20g fat,
    4g fiber. Mediterranean Quinoa Salad: 320 calories per serving, 12g protein, 38g
    carbohydrates, 14g fat, 6g fiber. Spanish Seafood Paella: 450 calories per serving,
    28g protein, 58g carbohydrates, 12g fat, 3g fiber. All recipes are rich in vitamins,
    minerals, and heart-healthy fats characteristic of the Mediterranean diet.
    """
    story.append(Paragraph(nutrition, styles['BodyText']))
    
    doc.build(story)
    print(f"✅ Created: {filename}")


if __name__ == "__main__":
    print("🔨 Creating sample PDFs for testing...\n")
    
    try:
        create_business_report()
        create_research_paper()
        create_technical_manual()
        create_recipe_book()
        
        print("\n✅ All sample PDFs created successfully!")
        print(f"\nFiles created in: {FIXTURES_DIR}/")
        print("  - business_report.pdf")
        print("  - research_paper.pdf")
        print("  - technical_manual.pdf")
        print("  - recipe_book.pdf")
        print("\nYou can now test the RAG system with these diverse documents!")
        
    except Exception as e:
        print(f"\n❌ Error creating PDFs: {e}")
        print("Make sure reportlab is installed: pip install reportlab")
