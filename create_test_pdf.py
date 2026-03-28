#!/usr/bin/env python3
"""
Create a comprehensive investment textbook PDF for testing.
"""

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
except ImportError:
    print("Installing reportlab...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

import os

# Create fixtures directory
os.makedirs("backend/tests/fixtures", exist_ok=True)

# Create PDF
pdf_path = "backend/tests/fixtures/investment.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter)
story = []

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor='darkblue',
    spaceAfter=30,
    alignment=TA_CENTER
)
heading_style = styles['Heading2']
body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=11,
    alignment=TA_JUSTIFY,
    spaceAfter=12
)

# Title Page
story.append(Paragraph("Investment Fundamentals", title_style))
story.append(Spacer(1, 0.5*inch))
story.append(Paragraph("A Comprehensive Guide to Stock Market Investing", styles['Heading3']))
story.append(PageBreak())

# Chapter 1: Theory of Diversification
story.append(Paragraph("Chapter 1: The Theory of Diversification", heading_style))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph(
    "Diversification is one of the most fundamental principles in investment management. "
    "The theory of diversification, first formalized by Harry Markowitz in 1952, states that "
    "investors can reduce portfolio risk by holding a variety of assets that are not perfectly correlated.",
    body_style
))

story.append(Paragraph(
    "The key insight is that while individual securities may be volatile, a portfolio of diverse "
    "securities can have lower overall volatility. This is because when some investments decline, "
    "others may rise or remain stable, offsetting losses. The mathematical foundation shows that "
    "portfolio risk depends not just on individual asset risks, but also on how assets move together.",
    body_style
))

story.append(Paragraph(
    "Modern Portfolio Theory demonstrates that diversification can eliminate unsystematic risk "
    "(company-specific risk) while systematic risk (market risk) remains. An optimal portfolio "
    "balances expected returns against risk through strategic diversification across asset classes, "
    "sectors, and geographic regions.",
    body_style
))

story.append(PageBreak())

# Chapter 2: The Eggs in One Basket Analogy
story.append(Paragraph("Chapter 2: Don't Put All Your Eggs in One Basket", heading_style))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph(
    "The famous saying 'don't put all your eggs in one basket' perfectly captures the essence "
    "of diversification. If you carry all your eggs in a single basket and drop it, you lose "
    "everything. However, if you distribute eggs across multiple baskets, dropping one basket "
    "results in only a partial loss.",
    body_style
))

story.append(Paragraph(
    "In investment terms, this means avoiding concentration risk. Investors who put all their "
    "money into a single stock, sector, or asset class face catastrophic losses if that investment "
    "fails. Historical examples include Enron employees who held most of their retirement savings "
    "in company stock, losing everything when the company collapsed.",
    body_style
))

story.append(Paragraph(
    "The analogy extends beyond just holding multiple stocks. True diversification requires "
    "spreading investments across different asset classes (stocks, bonds, real estate), sectors "
    "(technology, healthcare, energy), geographic regions (domestic and international), and "
    "investment styles (growth and value). This multi-dimensional approach provides robust "
    "protection against various market scenarios.",
    body_style
))

story.append(PageBreak())

# Chapter 3: Dealing with Brokerage Houses
story.append(Paragraph("Chapter 3: How to Deal with Brokerage Houses", heading_style))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph(
    "Brokerage houses serve as intermediaries between investors and financial markets. Choosing "
    "the right broker is crucial for investment success. There are two main types: full-service "
    "brokers who provide research, advice, and portfolio management, and discount brokers who "
    "offer lower fees but minimal guidance.",
    body_style
))

story.append(Paragraph(
    "When selecting a brokerage house, consider several factors: commission structure and fees, "
    "trading platform quality, research and educational resources, customer service, account "
    "minimums, and regulatory compliance. Compare multiple brokers before committing, as fees "
    "can significantly impact long-term returns.",
    body_style
))

story.append(Paragraph(
    "Modern investors should verify that brokers are registered with FINRA (Financial Industry "
    "Regulatory Authority) and protected by SIPC (Securities Investor Protection Corporation) "
    "insurance. Read all account agreements carefully, understand margin requirements if trading "
    "on margin, and be aware of any conflicts of interest such as payment for order flow.",
    body_style
))

story.append(Paragraph(
    "Establish clear communication with your broker. Ask questions about fees, execution quality, "
    "and investment recommendations. Keep detailed records of all transactions and statements. "
    "If problems arise, escalate through the broker's complaint process and contact FINRA if "
    "necessary. Remember, you are the client and have the right to transparent, fair treatment.",
    body_style
))

story.append(PageBreak())

# Chapter 4: Becoming an Intelligent Investor
story.append(Paragraph("Chapter 4: How to Become an Intelligent Investor", heading_style))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph(
    "Benjamin Graham's concept of the 'intelligent investor' emphasizes rational, disciplined "
    "decision-making over emotional reactions. Intelligent investors distinguish between investment "
    "(buying based on thorough analysis) and speculation (buying based on price predictions).",
    body_style
))

story.append(Paragraph(
    "The foundation of intelligent investing is education. Study financial statements, understand "
    "valuation metrics like P/E ratios and price-to-book ratios, and learn economic principles. "
    "Read annual reports, follow market news critically, and continuously expand your knowledge "
    "through books, courses, and reputable financial publications.",
    body_style
))

story.append(Paragraph(
    "Develop a long-term perspective. Intelligent investors focus on business fundamentals rather "
    "than short-term price movements. They practice patience, avoid market timing, and resist "
    "the urge to follow trends. Warren Buffett's advice to 'be fearful when others are greedy "
    "and greedy when others are fearful' embodies this contrarian, rational approach.",
    body_style
))

story.append(Paragraph(
    "Implement a systematic investment process: define clear goals, establish risk tolerance, "
    "create an asset allocation strategy, research investments thoroughly, maintain discipline "
    "during volatility, and regularly review and rebalance your portfolio. Intelligent investors "
    "also recognize their limitations and seek professional advice when needed.",
    body_style
))

story.append(PageBreak())

# Chapter 5: Business Valuation Methods
story.append(Paragraph("Chapter 5: How to Do Business Valuation", heading_style))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph(
    "Business valuation is the process of determining a company's economic worth. Several methods "
    "exist, each with strengths and limitations. The three primary approaches are asset-based, "
    "income-based, and market-based valuation.",
    body_style
))

story.append(Paragraph(
    "The Discounted Cash Flow (DCF) method is the most theoretically sound income-based approach. "
    "It values a business by projecting future free cash flows and discounting them to present "
    "value using an appropriate discount rate (typically the weighted average cost of capital). "
    "The formula is: Company Value = Σ(FCF_t / (1+r)^t) where FCF is free cash flow, r is the "
    "discount rate, and t is the time period.",
    body_style
))

story.append(Paragraph(
    "Market-based valuation uses comparable company analysis. Identify similar publicly traded "
    "companies and calculate valuation multiples like P/E (Price-to-Earnings), EV/EBITDA "
    "(Enterprise Value to Earnings Before Interest, Taxes, Depreciation, and Amortization), "
    "and Price-to-Sales ratios. Apply these multiples to the target company's metrics to "
    "estimate value.",
    body_style
))

story.append(Paragraph(
    "Asset-based valuation calculates net asset value by subtracting liabilities from assets. "
    "This method works well for asset-heavy businesses but may undervalue companies with "
    "significant intangible assets like brands or intellectual property. Adjust book values "
    "to fair market values for accuracy.",
    body_style
))

story.append(Paragraph(
    "In practice, use multiple valuation methods and triangulate to a reasonable range. Consider "
    "qualitative factors like management quality, competitive advantages, industry trends, and "
    "growth prospects. Remember that valuation is part art, part science—different assumptions "
    "yield different results, so sensitivity analysis is essential.",
    body_style
))

story.append(PageBreak())

# Chapter 6: Risk and Return
story.append(Paragraph("Chapter 6: Understanding Risk and Return", heading_style))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph(
    "The relationship between risk and return is fundamental to investing. Generally, higher "
    "potential returns come with higher risk. Risk represents the uncertainty of returns and "
    "the possibility of losing principal. Return is the gain or loss on an investment over time.",
    body_style
))

story.append(Paragraph(
    "Different asset classes have different risk-return profiles. Stocks historically offer "
    "higher returns but greater volatility. Bonds provide more stable income with lower returns. "
    "Cash equivalents offer safety but minimal returns, often below inflation. Real estate and "
    "alternative investments fall somewhere in between.",
    body_style
))

story.append(Paragraph(
    "Risk tolerance varies by individual based on age, financial situation, goals, and "
    "psychological factors. Younger investors can typically accept more risk due to longer "
    "time horizons. Those nearing retirement should prioritize capital preservation. Assess "
    "your risk tolerance honestly before investing.",
    body_style
))

story.append(PageBreak())

# Chapter 7: Asset Allocation
story.append(Paragraph("Chapter 7: Strategic Asset Allocation", heading_style))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph(
    "Asset allocation—dividing investments among different asset categories—is the primary "
    "determinant of portfolio returns. Studies show that over 90% of portfolio performance "
    "variability comes from asset allocation decisions rather than individual security selection.",
    body_style
))

story.append(Paragraph(
    "A common rule of thumb is the '100 minus age' rule: subtract your age from 100 to determine "
    "the percentage to allocate to stocks, with the remainder in bonds. For example, a 30-year-old "
    "might hold 70% stocks and 30% bonds. However, this is just a starting point—adjust based on "
    "personal circumstances.",
    body_style
))

story.append(Paragraph(
    "Rebalancing maintains your target allocation. Over time, winning investments grow to "
    "represent larger portfolio percentages, increasing risk. Rebalancing involves selling "
    "outperformers and buying underperformers, enforcing the discipline of 'buy low, sell high.' "
    "Rebalance annually or when allocations drift 5% or more from targets.",
    body_style
))

# Build PDF
doc.build(story)

print(f"✅ Created comprehensive investment PDF: {pdf_path}")
print(f"📄 File size: {os.path.getsize(pdf_path) / 1024:.1f} KB")
print(f"📚 Content includes:")
print("   - Theory of Diversification")
print("   - Eggs in One Basket Analogy")
print("   - Dealing with Brokerage Houses")
print("   - Becoming an Intelligent Investor")
print("   - Business Valuation Methods")
print("   - Risk and Return")
print("   - Asset Allocation")
