"""
NAR Code of Ethics Articles
Simplified summaries for complaint filing assistance
"""

NAR_CODE_ARTICLES = {
    "Article 1": {
        "title": "Duties to Clients and Customers",
        "summary": "REALTORS® must protect and promote the interests of their client while treating all parties honestly.",
        "common_violations": [
            "Failing to disclose conflicts of interest",
            "Not acting in client's best interest",
            "Providing false or misleading information"
        ]
    },
    "Article 2": {
        "title": "Avoiding Exaggeration, Misrepresentation, or Concealment",
        "summary": "REALTORS® must avoid exaggeration, misrepresentation, or concealment of pertinent facts.",
        "common_violations": [
            "Misrepresenting property condition",
            "Concealing material facts",
            "Exaggerating property features or value"
        ]
    },
    "Article 3": {
        "title": "Cooperation with Other REALTORS®",
        "summary": "REALTORS® must cooperate with other brokers when in the client's best interest.",
        "common_violations": [
            "Refusing to show properties without justification",
            "Withholding property information",
            "Failing to present all offers"
        ]
    },
    "Article 4": {
        "title": "Disclosure of Information",
        "summary": "REALTORS® must disclose facts that could adversely affect parties' ability or desire to complete a transaction.",
        "common_violations": [
            "Not disclosing dual agency",
            "Hiding commission arrangements",
            "Failing to disclose material defects"
        ]
    },
    "Article 5": {
        "title": "No Uninvited Solicitation",
        "summary": "REALTORS® must not solicit property listed exclusively with another broker without consent.",
        "common_violations": [
            "Contacting sellers with exclusive listings",
            "Attempting to procure listings already under contract",
            "Interfering with existing broker relationships"
        ]
    },
    "Article 6": {
        "title": "Compensation Disclosure",
        "summary": "REALTORS® must disclose their status and any expected compensation from transactions.",
        "common_violations": [
            "Not disclosing dual compensation",
            "Accepting undisclosed referral fees",
            "Hidden commission arrangements"
        ]
    },
    "Article 7": {
        "title": "Accepting Compensation",
        "summary": "REALTORS® must accept compensation only from their client or with client's knowledge.",
        "common_violations": [
            "Accepting kickbacks",
            "Taking fees from service providers without disclosure",
            "Secret profit arrangements"
        ]
    },
    "Article 8": {
        "title": "Obtaining Consent for Services",
        "summary": "REALTORS® must keep clients informed and obtain consent for services performed.",
        "common_violations": [
            "Making unauthorized decisions",
            "Incurring expenses without approval",
            "Binding clients without authority"
        ]
    },
    "Article 9": {
        "title": "Obligation to Preserve Confidential Information",
        "summary": "REALTORS® must preserve client confidences unless disclosure is required by law or authorized.",
        "common_violations": [
            "Revealing client's negotiating position",
            "Disclosing confidential financial information",
            "Sharing private client details without permission"
        ]
    },
    "Article 10": {
        "title": "Duties in Presenting Offers",
        "summary": "REALTORS® must present all offers objectively and as quickly as possible.",
        "common_violations": [
            "Withholding or delaying offers",
            "Refusing to present competing offers",
            "Pressuring clients to reject offers"
        ]
    },
    "Article 11": {
        "title": "Competence in Specialized Fields",
        "summary": "REALTORS® must seek assistance for services outside their competence.",
        "common_violations": [
            "Providing legal or tax advice without qualification",
            "Practicing outside area of expertise",
            "Not referring to appropriate specialists"
        ]
    },
    "Article 12": {
        "title": "Truthful Advertising",
        "summary": "REALTORS® must present a true picture in advertising and avoid misleading statements.",
        "common_violations": [
            "False property descriptions",
            "Misleading photos or claims",
            "Bait-and-switch advertising"
        ]
    },
    "Article 13": {
        "title": "No False or Misleading Representations",
        "summary": "REALTORS® must not engage in practices that mislead the public.",
        "common_violations": [
            "False credentials or designations",
            "Misrepresenting market conditions",
            "Deceptive business practices"
        ]
    },
    "Article 14": {
        "title": "Respect for Exclusive Relationships",
        "summary": "REALTORS® must respect exclusive representation relationships with other brokers' clients.",
        "common_violations": [
            "Contacting exclusively represented buyers/sellers",
            "Attempting to establish competing relationships",
            "Interfering with exclusive agreements"
        ]
    },
    "Article 15": {
        "title": "No Misrepresentation About Property",
        "summary": "REALTORS® must not knowingly or recklessly make false statements about property or transactions.",
        "common_violations": [
            "Lying about property status",
            "False claims about offers received",
            "Misrepresenting transaction terms"
        ]
    },
    "Article 16": {
        "title": "Respect for Other Professionals",
        "summary": "REALTORS® must not engage in practices that harm other professionals' reputations or businesses.",
        "common_violations": [
            "Making unfounded criticisms of competitors",
            "Disparaging other REALTORS®",
            "Unfair competitive practices"
        ]
    },
    "Article 17": {
        "title": "Arbitration of Disputes",
        "summary": "REALTORS® must arbitrate contractual disputes with other REALTORS® when requested.",
        "common_violations": [
            "Refusing mandatory arbitration",
            "Not complying with arbitration decisions",
            "Avoiding dispute resolution processes"
        ]
    }
}


def get_all_articles():
    """Return all NAR Code articles"""
    return NAR_CODE_ARTICLES


def get_article(article_number):
    """Get specific article by number"""
    return NAR_CODE_ARTICLES.get(article_number)


def search_articles(keyword):
    """Search articles by keyword in title, summary, or violations"""
    keyword = keyword.lower()
    results = []

    for article_num, article_data in NAR_CODE_ARTICLES.items():
        if (keyword in article_data['title'].lower() or
            keyword in article_data['summary'].lower() or
            any(keyword in violation.lower() for violation in article_data['common_violations'])):
            results.append({
                'article': article_num,
                'data': article_data
            })

    return results


def get_articles_list():
    """Return simplified list for dropdown/selection"""
    return [
        {
            'value': article_num,
            'label': f"{article_num}: {article_data['title']}"
        }
        for article_num, article_data in NAR_CODE_ARTICLES.items()
    ]
