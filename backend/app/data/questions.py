"""Question definitions and dimension metadata for the compatibility questionnaire."""

DIMENSIONS = {
    "communication": {
        "id": "communication",
        "name": "Communication",
        "description": "How openly, directly, and constructively you express thoughts, feelings, and expectations.",
        "icon": "chat-bubble",
        "weight": 0.18,
    },
    "emotional_openness": {
        "id": "emotional_openness",
        "name": "Emotional Openness",
        "description": "Vulnerability, self-awareness, and readiness to share sensitive emotional states.",
        "icon": "heart",
        "weight": 0.12,
    },
    "social_nature": {
        "id": "social_nature",
        "name": "Social Nature",
        "description": "Social energy preferences, circle of friends, and balance of public vs. private time.",
        "icon": "users",
        "weight": 0.05,
    },
    "independence": {
        "id": "independence",
        "name": "Independence",
        "description": "Value placed on autonomy, personal space, individual hobbies, and decision independence.",
        "icon": "compass",
        "weight": 0.05,
    },
    "family_orientation": {
        "id": "family_orientation",
        "name": "Family Orientation",
        "description": "Priority of family bonds, involvement in extended family, traditions, and future family life.",
        "icon": "home",
        "weight": 0.12,
    },
    "financial_attitude": {
        "id": "financial_attitude",
        "name": "Financial Attitude",
        "description": "Prudence in spending, saving habits, financial ambition, and openness regarding shared money.",
        "icon": "cash",
        "weight": 0.14,
    },
    "career_orientation": {
        "id": "career_orientation",
        "name": "Career Orientation",
        "description": "Professional ambition, dedication to career growth, work-life balance, and relocation flexibility.",
        "icon": "briefcase",
        "weight": 0.06,
    },
    "adventure": {
        "id": "adventure",
        "name": "Adventure & Spontaneity",
        "description": "Desire for novelty, spontaneous travel, risk tolerance, and trying unfamiliar experiences.",
        "icon": "sparkles",
        "weight": 0.04,
    },
    "conflict_handling": {
        "id": "conflict_handling",
        "name": "Conflict Handling",
        "description": "Approach to disagreements, de-escalation, emotional regulation, and finding collaborative solutions.",
        "icon": "scale",
        "weight": 0.16,
    },
    "lifestyle_preference": {
        "id": "lifestyle_preference",
        "name": "Lifestyle & Routine",
        "description": "Daily structure, domestic habits, health preferences, predictability, and organization.",
        "icon": "sun",
        "weight": 0.08,
    },
}

QUESTIONS = [
    # ── Dimension 1: Communication (Q1 - Q4) ──
    {
        "id": 1,
        "dimension": "communication",
        "dimension_name": "Communication",
        "question": "When you have a serious disagreement with someone close to you, what do you usually do?",
        "options": [
            {"id": "A", "text": "Initiate a calm, direct conversation as soon as possible"},
            {"id": "B", "text": "Take a short pause to collect thoughts, then discuss thoroughly"},
            {"id": "C", "text": "Drop subtle hints and wait for the other person to raise it"},
            {"id": "D", "text": "Keep quiet and hope the issue resolves itself over time"},
        ],
        "scores": {
            "A": {"communication": 5, "conflict_handling": 4},
            "B": {"communication": 4, "conflict_handling": 5},
            "C": {"communication": 2, "conflict_handling": 2},
            "D": {"communication": 1, "conflict_handling": 1},
        },
    },
    {
        "id": 2,
        "dimension": "communication",
        "dimension_name": "Communication",
        "question": "If your partner unintentionally says something that hurts your feelings, your first response is to:",
        "options": [
            {"id": "A", "text": "Express how the statement felt in an honest, non-defensive way"},
            {"id": "B", "text": "Reflect on why it hurt before deciding whether it needs discussing"},
            {"id": "C", "text": "Pull back emotionally and become quiet for the rest of the day"},
            {"id": "D", "text": "Make a sarcastic remark or brush it off while feeling resentful"},
        ],
        "scores": {
            "A": {"communication": 5, "emotional_openness": 4},
            "B": {"communication": 4, "emotional_openness": 3},
            "C": {"communication": 2, "emotional_openness": 2},
            "D": {"communication": 1, "emotional_openness": 1},
        },
    },
    {
        "id": 3,
        "dimension": "communication",
        "dimension_name": "Communication",
        "question": "How do you prefer to discuss sensitive relationship topics (e.g. boundaries, expectations)?",
        "options": [
            {"id": "A", "text": "Regular proactive check-ins where both can speak freely"},
            {"id": "B", "text": "Address them whenever specific situations naturally arise"},
            {"id": "C", "text": "Prefer written messages or texts to avoid confrontation"},
            {"id": "D", "text": "Rarely bring them up unless there is an absolute crisis"},
        ],
        "scores": {
            "A": {"communication": 5, "emotional_openness": 5},
            "B": {"communication": 4, "emotional_openness": 3},
            "C": {"communication": 2, "emotional_openness": 2},
            "D": {"communication": 1, "emotional_openness": 1},
        },
    },
    {
        "id": 4,
        "dimension": "communication",
        "dimension_name": "Communication",
        "question": "When you and your partner hold opposing opinions on an important issue, you focus on:",
        "options": [
            {"id": "A", "text": "Active listening to understand their worldview before stating your own"},
            {"id": "B", "text": "Finding logical middle ground where both make sensible compromises"},
            {"id": "C", "text": "Defending your position firmly until they see the flaw in theirs"},
            {"id": "D", "text": "Agreeing outwardly just to end the tension, while disagreeing internally"},
        ],
        "scores": {
            "A": {"communication": 5, "conflict_handling": 5},
            "B": {"communication": 4, "conflict_handling": 4},
            "C": {"communication": 2, "conflict_handling": 1},
            "D": {"communication": 1, "conflict_handling": 2},
        },
    },

    # ── Dimension 2: Emotional Openness (Q5 - Q8) ──
    {
        "id": 5,
        "dimension": "emotional_openness",
        "dimension_name": "Emotional Openness",
        "question": "When facing personal stress or self-doubt, how comfortable are you sharing it with a partner?",
        "options": [
            {"id": "A", "text": "Completely transparent; I openly share my fears and vulnerabilities"},
            {"id": "B", "text": "Share once I have processed the initial emotions on my own"},
            {"id": "C", "text": "Only share high-level facts, keeping deep feelings guarded"},
            {"id": "D", "text": "Conceal it completely; I dislike appearing vulnerable or dependent"},
        ],
        "scores": {
            "A": {"emotional_openness": 5},
            "B": {"emotional_openness": 4},
            "C": {"emotional_openness": 2},
            "D": {"emotional_openness": 1},
        },
    },
    {
        "id": 6,
        "dimension": "emotional_openness",
        "dimension_name": "Emotional Openness",
        "question": "How do you respond when your partner is visibly overwhelmed or crying?",
        "options": [
            {"id": "A", "text": "Hold empathetic space, listen patiently, and validate their feelings"},
            {"id": "B", "text": "Comfort them and gently offer practical solutions or action plans"},
            {"id": "C", "text": "Feel slightly awkward but stay present to do whatever they request"},
            {"id": "D", "text": "Feel uncomfortable and look for a way to give them space or step away"},
        ],
        "scores": {
            "A": {"emotional_openness": 5, "communication": 4},
            "B": {"emotional_openness": 4, "communication": 4},
            "C": {"emotional_openness": 2, "communication": 2},
            "D": {"emotional_openness": 1, "communication": 1},
        },
    },
    {
        "id": 7,
        "dimension": "emotional_openness",
        "dimension_name": "Emotional Openness",
        "question": "Expressing gratitude, affection, and emotional warmth verbally is:",
        "options": [
            {"id": "A", "text": "Natural and frequent; I say 'I appreciate you' daily"},
            {"id": "B", "text": "Meaningful and stated regularly during special or quiet moments"},
            {"id": "C", "text": "Expressed through actions and deeds rather than frequent words"},
            {"id": "D", "text": "Rare; emotional verbal declarations feel awkward or unnecessary"},
        ],
        "scores": {
            "A": {"emotional_openness": 5},
            "B": {"emotional_openness": 4},
            "C": {"emotional_openness": 3},
            "D": {"emotional_openness": 1},
        },
    },
    {
        "id": 8,
        "dimension": "emotional_openness",
        "dimension_name": "Emotional Openness",
        "question": "When reflecting on painful experiences from your past:",
        "options": [
            {"id": "A", "text": "I can talk openly about lessons learned and my lingering vulnerabilities"},
            {"id": "B", "text": "I can discuss them when deep trust and psychological safety exist"},
            {"id": "C", "text": "I prefer to leave the past in the past and rarely revisit old wounds"},
            {"id": "D", "text": "I lock them away and strongly resent anyone probing into them"},
        ],
        "scores": {
            "A": {"emotional_openness": 5},
            "B": {"emotional_openness": 4},
            "C": {"emotional_openness": 2},
            "D": {"emotional_openness": 1},
        },
    },

    # ── Dimension 3: Social Nature (Q9 - Q12) ──
    {
        "id": 9,
        "dimension": "social_nature",
        "dimension_name": "Social Nature",
        "question": "After a demanding work week, your ideal Friday evening looks like:",
        "options": [
            {"id": "A", "text": "A bustling dinner or party with a large group of friends and acquaintances"},
            {"id": "B", "text": "A relaxed gathering with a few close, intimate friends"},
            {"id": "C", "text": "Quiet dinner with my partner or solitary time watching movies/reading"},
            {"id": "D", "text": "Complete solitude in my own space with zero social interaction"},
        ],
        "scores": {
            "A": {"social_nature": 5, "independence": 2},
            "B": {"social_nature": 4, "independence": 3},
            "C": {"social_nature": 2, "independence": 4},
            "D": {"social_nature": 1, "independence": 5},
        },
    },
    {
        "id": 10,
        "dimension": "social_nature",
        "dimension_name": "Social Nature",
        "question": "When your partner wants to host a lively dinner with friends at your home:",
        "options": [
            {"id": "A", "text": "Thrilled! I love being the host and having our home filled with people"},
            {"id": "B", "text": "Happy to host occasionally, provided we plan and wrap up at a decent hour"},
            {"id": "C", "text": "I will participate politely, but home is primarily my sanctuary to rest"},
            {"id": "D", "text": "Strongly prefer keeping social gatherings strictly outside our house"},
        ],
        "scores": {
            "A": {"social_nature": 5},
            "B": {"social_nature": 4},
            "C": {"social_nature": 2},
            "D": {"social_nature": 1},
        },
    },
    {
        "id": 11,
        "dimension": "social_nature",
        "dimension_name": "Social Nature",
        "question": "Making new acquaintances and expanding your professional/personal network is:",
        "options": [
            {"id": "A", "text": "Energizing; I genuinely enjoy striking up conversations with strangers"},
            {"id": "B", "text": "Pleasant and natural when connected through shared interests or work"},
            {"id": "C", "text": "Tiring; I stick strictly to my existing circle of trusted people"},
            {"id": "D", "text": "Draining and something I consciously avoid whenever possible"},
        ],
        "scores": {
            "A": {"social_nature": 5},
            "B": {"social_nature": 4},
            "C": {"social_nature": 2},
            "D": {"social_nature": 1},
        },
    },
    {
        "id": 12,
        "dimension": "social_nature",
        "dimension_name": "Social Nature",
        "question": "How should social commitments (weddings, parties, reunions) be balanced?",
        "options": [
            {"id": "A", "text": "Say yes to almost every invitation—life is richer when socially connected"},
            {"id": "B", "text": "Prioritize important milestones and maintain a consistent social cadence"},
            {"id": "C", "text": "Attend only when obligatory; protect couple and downtime jealously"},
            {"id": "D", "text": "Decline the vast majority; we both thrive most in quiet seclusion"},
        ],
        "scores": {
            "A": {"social_nature": 5},
            "B": {"social_nature": 4},
            "C": {"social_nature": 2},
            "D": {"social_nature": 1},
        },
    },

    # ── Dimension 4: Independence (Q13 - Q16) ──
    {
        "id": 13,
        "dimension": "independence",
        "dimension_name": "Independence",
        "question": "In a committed relationship, spending full weekends or vacations apart on personal hobbies:",
        "options": [
            {"id": "A", "text": "Essential for personal vitality and individual growth"},
            {"id": "B", "text": "Healthy and welcome on occasion with open communication"},
            {"id": "C", "text": "Acceptable for brief periods, but vacations should primarily be together"},
            {"id": "D", "text": "Unsettling; I believe partners should share all key leisure time together"},
        ],
        "scores": {
            "A": {"independence": 5},
            "B": {"independence": 4},
            "C": {"independence": 2},
            "D": {"independence": 1},
        },
    },
    {
        "id": 14,
        "dimension": "independence",
        "dimension_name": "Independence",
        "question": "When making an everyday personal purchase or scheduling personal plans:",
        "options": [
            {"id": "A", "text": "I make individual decisions independently without needing consultation"},
            {"id": "B", "text": "I mention it casually out of courtesy, but retain full decision autonomy"},
            {"id": "C", "text": "I prefer checking in with my partner beforehand to ensure alignment"},
            {"id": "D", "text": "I consult on virtually everything to ensure we act as a singular unit"},
        ],
        "scores": {
            "A": {"independence": 5},
            "B": {"independence": 4},
            "C": {"independence": 2},
            "D": {"independence": 1},
        },
    },
    {
        "id": 15,
        "dimension": "independence",
        "dimension_name": "Independence",
        "question": "How important is having distinct personal hobbies and friends separate from your partner?",
        "options": [
            {"id": "A", "text": "Crucial; having a distinct identity prevents codependency"},
            {"id": "B", "text": "Very healthy; balanced blend of shared activities and individual pursuits"},
            {"id": "C", "text": "Nice to have, but I naturally prefer integrating our interests and circles"},
            {"id": "D", "text": "Low priority; my dream is doing almost everything together"},
        ],
        "scores": {
            "A": {"independence": 5},
            "B": {"independence": 4},
            "C": {"independence": 2},
            "D": {"independence": 1},
        },
    },
    {
        "id": 16,
        "dimension": "independence",
        "dimension_name": "Independence",
        "question": "When your partner is away on a solo trip for a week, you generally feel:",
        "options": [
            {"id": "A", "text": "Energized to enjoy solo projects, recharge, and relish the solitude"},
            {"id": "B", "text": "Comfortable and productive, while exchanging sweet daily updates"},
            {"id": "C", "text": "Slightly lonely and eagerly counting down the days until they return"},
            {"id": "D", "text": "Anxious or restless; I struggle to feel at ease when we are separated"},
        ],
        "scores": {
            "A": {"independence": 5},
            "B": {"independence": 4},
            "C": {"independence": 2},
            "D": {"independence": 1},
        },
    },

    # ── Dimension 5: Family Orientation (Q17 - Q20) ──
    {
        "id": 17,
        "dimension": "family_orientation",
        "dimension_name": "Family Orientation",
        "question": "How frequently do you envision interacting with extended family (parents, siblings, in-laws)?",
        "options": [
            {"id": "A", "text": "Very frequently (weekly visits or calls, close-knit integration in daily life)"},
            {"id": "B", "text": "Regularly (a few times a month, celebrating holidays and milestones)"},
            {"id": "C", "text": "Occasionally (major holidays and birthdays, keeping clear boundaries)"},
            {"id": "D", "text": "Rarely (independent nuclear life with minimal extended family involvement)"},
        ],
        "scores": {
            "A": {"family_orientation": 5},
            "B": {"family_orientation": 4},
            "C": {"family_orientation": 2},
            "D": {"family_orientation": 1},
        },
    },
    {
        "id": 18,
        "dimension": "family_orientation",
        "dimension_name": "Family Orientation",
        "question": "When family members express strong opinions regarding your relationship choices:",
        "options": [
            {"id": "A", "text": "We deeply honor their counsel and weigh their blessings very heavily"},
            {"id": "B", "text": "We listen respectfully, while making the ultimate decision as a couple"},
            {"id": "C", "text": "We set firm boundaries; couple autonomy takes precedence over family input"},
            {"id": "D", "text": "We dismiss unsolicited family opinions immediately to protect our privacy"},
        ],
        "scores": {
            "A": {"family_orientation": 5},
            "B": {"family_orientation": 4},
            "C": {"family_orientation": 2},
            "D": {"family_orientation": 1},
        },
    },
    {
        "id": 19,
        "dimension": "family_orientation",
        "dimension_name": "Family Orientation",
        "question": "Regarding children and parenting in long-term life plans:",
        "options": [
            {"id": "A", "text": "Raising a family is a central, cherished life goal and top priority"},
            {"id": "B", "text": "Very positive toward children when emotional and financial timing aligns"},
            {"id": "C", "text": "Undecided or open to a child-free lifestyle focused on couple goals"},
            {"id": "D", "text": "Clear preference for a child-free life dedicated to personal and career freedom"},
        ],
        "scores": {
            "A": {"family_orientation": 5},
            "B": {"family_orientation": 4},
            "C": {"family_orientation": 2},
            "D": {"family_orientation": 1},
        },
    },
    {
        "id": 20,
        "dimension": "family_orientation",
        "dimension_name": "Family Orientation",
        "question": "If an elderly parent or family member needs long-term care or support:",
        "options": [
            {"id": "A", "text": "I would naturally welcome them into our home or provide direct daily care"},
            {"id": "B", "text": "Provide substantial physical, financial, and emotional support cooperatively"},
            {"id": "C", "text": "Arrange professional elder care while preserving our household boundaries"},
            {"id": "D", "text": "Expect them to manage their own elder care arrangements independently"},
        ],
        "scores": {
            "A": {"family_orientation": 5},
            "B": {"family_orientation": 4},
            "C": {"family_orientation": 2},
            "D": {"family_orientation": 1},
        },
    },

    # ── Dimension 6: Financial Attitude (Q21 - Q24) ──
    {
        "id": 21,
        "dimension": "financial_attitude",
        "dimension_name": "Financial Attitude",
        "question": "You unexpectedly receive a bonus or windfall of $10,000 (or equivalent). You would most likely:",
        "options": [
            {"id": "A", "text": "Deposit into long-term savings, emergency funds, or low-risk index investments"},
            {"id": "B", "text": "Invest 70% in growth assets and allocate 30% for a rewarding experience"},
            {"id": "C", "text": "Use the majority for travel, gadgets, or memorable upgrades right away"},
            {"id": "D", "text": "Spend freely on immediate pleasures without detailed calculation"},
        ],
        "scores": {
            "A": {"financial_attitude": 5},
            "B": {"financial_attitude": 4},
            "C": {"financial_attitude": 2},
            "D": {"financial_attitude": 1},
        },
    },
    {
        "id": 22,
        "dimension": "financial_attitude",
        "dimension_name": "Financial Attitude",
        "question": "How do you believe long-term partners should manage their finances?",
        "options": [
            {"id": "A", "text": "Complete financial transparency with shared accounts and a unified budget"},
            {"id": "B", "text": "A joint account for mutual household expenses plus separate personal accounts"},
            {"id": "C", "text": "Mostly independent finances with proportional splitting of common bills"},
            {"id": "D", "text": "Strictly separate finances; money matters should remain private"},
        ],
        "scores": {
            "A": {"financial_attitude": 5, "communication": 4},
            "B": {"financial_attitude": 4, "independence": 4},
            "C": {"financial_attitude": 3, "independence": 5},
            "D": {"financial_attitude": 1, "independence": 5},
        },
    },
    {
        "id": 23,
        "dimension": "financial_attitude",
        "dimension_name": "Financial Attitude",
        "question": "When making large discretionary purchases (e.g., luxury goods, big tech, holidays):",
        "options": [
            {"id": "A", "text": "Always plan months ahead, comparison-shop, and discuss before committing"},
            {"id": "B", "text": "Check budget feasibility first; buy if it fits comfortably within savings"},
            {"id": "C", "text": "Occasionally make impulsive high-ticket buys if the excitement is high"},
            {"id": "D", "text": "Live in the moment; if funds exist or credit is available, go for it"},
        ],
        "scores": {
            "A": {"financial_attitude": 5},
            "B": {"financial_attitude": 4},
            "C": {"financial_attitude": 2},
            "D": {"financial_attitude": 1},
        },
    },
    {
        "id": 24,
        "dimension": "financial_attitude",
        "dimension_name": "Financial Attitude",
        "question": "Regarding debt (credit cards, loans, mortgages), your philosophy is:",
        "options": [
            {"id": "A", "text": "Zero tolerance for high-interest debt; payoff and security take absolute precedence"},
            {"id": "B", "text": "Strategic use of low-interest leverage (e.g. mortgage/education) with tight controls"},
            {"id": "C", "text": "Debt is normal and manageable as long as minimum payments are met"},
            {"id": "D", "text": "I rarely track debt specifics and prefer not to worry about financial constraints"},
        ],
        "scores": {
            "A": {"financial_attitude": 5},
            "B": {"financial_attitude": 4},
            "C": {"financial_attitude": 2},
            "D": {"financial_attitude": 1},
        },
    },

    # ── Dimension 7: Career Orientation (Q25 - Q28) ──
    {
        "id": 25,
        "dimension": "career_orientation",
        "dimension_name": "Career Orientation",
        "question": "Your professional ambitions and career milestones rank as:",
        "options": [
            {"id": "A", "text": "A primary defining pillar of my life and personal fulfillment"},
            {"id": "B", "text": "Very significant; I pursue steady career progression alongside personal life"},
            {"id": "C", "text": "Work is a practical means to fund life; work-life balance always comes first"},
            {"id": "D", "text": "Minimal ambition; I prefer low-stress work with zero overtime or pressure"},
        ],
        "scores": {
            "A": {"career_orientation": 5},
            "B": {"career_orientation": 4},
            "C": {"career_orientation": 2},
            "D": {"career_orientation": 1},
        },
    },
    {
        "id": 26,
        "dimension": "career_orientation",
        "dimension_name": "Career Orientation",
        "question": "Your partner receives an outstanding career promotion that requires moving to another city:",
        "options": [
            {"id": "A", "text": "Fully supportive; exciting career advancements justify relocating together"},
            {"id": "B", "text": "Deeply evaluate both career trajectories and find a balanced compromise"},
            {"id": "C", "text": "Reluctant; local stability and established roots matter more than promotions"},
            {"id": "D", "text": "Firmly oppose relocating for a partner's job; my roots must stay put"},
        ],
        "scores": {
            "A": {"career_orientation": 5, "adventure": 4},
            "B": {"career_orientation": 4, "communication": 4},
            "C": {"career_orientation": 2, "lifestyle_preference": 4},
            "D": {"career_orientation": 1, "lifestyle_preference": 5},
        },
    },
    {
        "id": 27,
        "dimension": "career_orientation",
        "dimension_name": "Career Orientation",
        "question": "When intense work demands require long hours, weekend sprints, or study:",
        "options": [
            {"id": "A", "text": "I embrace the hustle cheerfully; big dreams require seasonal sacrifices"},
            {"id": "B", "text": "Acceptable temporarily for milestone targets, followed by intentional rest"},
            {"id": "C", "text": "Frustrating; work should rarely encroach upon personal or relationship time"},
            {"id": "D", "text": "Unacceptable; strict boundary of 40 hours maximum under all circumstances"},
        ],
        "scores": {
            "A": {"career_orientation": 5},
            "B": {"career_orientation": 4},
            "C": {"career_orientation": 2},
            "D": {"career_orientation": 1},
        },
    },
    {
        "id": 28,
        "dimension": "career_orientation",
        "dimension_name": "Career Orientation",
        "question": "How important is it that your partner possesses strong drive and career ambition?",
        "options": [
            {"id": "A", "text": "Essential; ambition, intellect, and high drive are major attraction magnets"},
            {"id": "B", "text": "Important; I admire someone with purpose, stability, and professional pride"},
            {"id": "C", "text": "Secondary; warmth, kindness, and presence matter infinitely more"},
            {"id": "D", "text": "Prefer someone with low career stress who prioritizes home and leisure"},
        ],
        "scores": {
            "A": {"career_orientation": 5},
            "B": {"career_orientation": 4},
            "C": {"career_orientation": 2},
            "D": {"career_orientation": 1},
        },
    },

    # ── Dimension 8: Adventure & Spontaneity (Q29 - Q32) ──
    {
        "id": 29,
        "dimension": "adventure",
        "dimension_name": "Adventure & Spontaneity",
        "question": "It is Saturday morning with zero plans. Your partner suggests packing a bag for an unplanned road trip:",
        "options": [
            {"id": "A", "text": "Pack in 15 minutes! Spontaneous adventures make life exhilarating"},
            {"id": "B", "text": "Excited, but take an hour to verify reservations and key details first"},
            {"id": "C", "text": "Hesitant; I strongly prefer planned outings with advance itineraries"},
            {"id": "D", "text": "Decline; unexpected disruptions to my weekend routine cause stress"},
        ],
        "scores": {
            "A": {"adventure": 5},
            "B": {"adventure": 4},
            "C": {"adventure": 2},
            "D": {"adventure": 1},
        },
    },
    {
        "id": 30,
        "dimension": "adventure",
        "dimension_name": "Adventure & Spontaneity",
        "question": "When planning vacations or holidays, your preferred style is:",
        "options": [
            {"id": "A", "text": "Off-the-beaten-path expeditions, backpacking, or thrill activities in new lands"},
            {"id": "B", "text": "A vibrant mix of cultural discovery, sightseeing, and good downtime"},
            {"id": "C", "text": "Relaxing at an all-inclusive beach resort with minimal logistical hassle"},
            {"id": "D", "text": "Returning to comfortable, familiar spots I already know and love"},
        ],
        "scores": {
            "A": {"adventure": 5},
            "B": {"adventure": 4},
            "C": {"adventure": 2},
            "D": {"adventure": 1},
        },
    },
    {
        "id": 31,
        "dimension": "adventure",
        "dimension_name": "Adventure & Spontaneity",
        "question": "Trying unfamiliar ethnic cuisines, unusual activities, or extreme sports:",
        "options": [
            {"id": "A", "text": "Always eager to try anything once; variety is the spice of life"},
            {"id": "B", "text": "Willing and curious when accompanied by someone enthusiastic"},
            {"id": "C", "text": "Cautious; I stick mostly to familiar foods and safe activities"},
            {"id": "D", "text": "Resistant; I see no reason to take unnecessary risks or try things I dislike"},
        ],
        "scores": {
            "A": {"adventure": 5},
            "B": {"adventure": 4},
            "C": {"adventure": 2},
            "D": {"adventure": 1},
        },
    },
    {
        "id": 32,
        "dimension": "adventure",
        "dimension_name": "Adventure & Spontaneity",
        "question": "How do you feel about regular life unpredictability and spontaneous schedule changes?",
        "options": [
            {"id": "A", "text": "I thrive in dynamic, fluid environments; rigid routines feel stifling"},
            {"id": "B", "text": "I adapt easily, provided core goals and commitments remain respected"},
            {"id": "C", "text": "Mildly irritated; I appreciate advance notice and predictable rhythm"},
            {"id": "D", "text": "Deeply unsettled; sudden changes cause significant friction for me"},
        ],
        "scores": {
            "A": {"adventure": 5, "lifestyle_preference": 1},
            "B": {"adventure": 4, "lifestyle_preference": 3},
            "C": {"adventure": 2, "lifestyle_preference": 4},
            "D": {"adventure": 1, "lifestyle_preference": 5},
        },
    },

    # ── Dimension 9: Conflict Handling (Q33 - Q36) ──
    {
        "id": 33,
        "dimension": "conflict_handling",
        "dimension_name": "Conflict Handling",
        "question": "During a heated disagreement, if tempers flare and voices begin to rise:",
        "options": [
            {"id": "A", "text": "Take a deep breath, de-escalate with empathy, and suggest a 10-minute pause"},
            {"id": "B", "text": "Stay focused strictly on facts and resolution without getting personally insulting"},
            {"id": "C", "text": "Match the emotional intensity and argue forcefully to defend my dignity"},
            {"id": "D", "text": "Shut down completely, walk out of the room, or give the silent treatment"},
        ],
        "scores": {
            "A": {"conflict_handling": 5, "emotional_openness": 4},
            "B": {"conflict_handling": 4, "emotional_openness": 3},
            "C": {"conflict_handling": 2, "emotional_openness": 2},
            "D": {"conflict_handling": 1, "emotional_openness": 1},
        },
    },
    {
        "id": 34,
        "dimension": "conflict_handling",
        "dimension_name": "Conflict Handling",
        "question": "After an argument concludes and an apology is made, how easily do you move forward?",
        "options": [
            {"id": "A", "text": "Quickly and genuinely; once reconciled, the slate is clean with zero grudges"},
            {"id": "B", "text": "Smoothly after a few hours of normal interaction rebuilds warmth"},
            {"id": "C", "text": "Slowly; emotional residue lingers for several days despite the apology"},
            {"id": "D", "text": "With difficulty; past grievances are stored and resurface during future fights"},
        ],
        "scores": {
            "A": {"conflict_handling": 5},
            "B": {"conflict_handling": 4},
            "C": {"conflict_handling": 2},
            "D": {"conflict_handling": 1},
        },
    },
    {
        "id": 35,
        "dimension": "conflict_handling",
        "dimension_name": "Conflict Handling",
        "question": "When you realize during an argument that you were factually mistaken or in the wrong:",
        "options": [
            {"id": "A", "text": "Admit it immediately and sincerely apologize without making excuses"},
            {"id": "B", "text": "Acknowledge the mistake calmly and refocus on fixing the problem"},
            {"id": "C", "text": "Deflect or minimize the mistake to avoid losing the upper hand"},
            {"id": "D", "text": "Double down and refuse to concede under any circumstances"},
        ],
        "scores": {
            "A": {"conflict_handling": 5, "communication": 5},
            "B": {"conflict_handling": 4, "communication": 4},
            "C": {"conflict_handling": 2, "communication": 2},
            "D": {"conflict_handling": 1, "communication": 1},
        },
    },
    {
        "id": 36,
        "dimension": "conflict_handling",
        "dimension_name": "Conflict Handling",
        "question": "What is your primary goal when managing relationship conflicts?",
        "options": [
            {"id": "A", "text": "Mutual emotional reconnection and deeper shared understanding"},
            {"id": "B", "text": "Practical, fair problem-solving where both sides compromise"},
            {"id": "C", "text": "Ensuring my partner understands my hurt and validates my perspective"},
            {"id": "D", "text": "Ending the unpleasantness as quickly as possible, regardless of resolution"},
        ],
        "scores": {
            "A": {"conflict_handling": 5, "emotional_openness": 5},
            "B": {"conflict_handling": 4, "communication": 4},
            "C": {"conflict_handling": 2, "communication": 2},
            "D": {"conflict_handling": 1, "communication": 1},
        },
    },

    # ── Dimension 10: Lifestyle & Routine (Q37 - Q40) ──
    {
        "id": 37,
        "dimension": "lifestyle_preference",
        "dimension_name": "Lifestyle & Routine",
        "question": "Regarding household cleanliness, tidiness, and organization:",
        "options": [
            {"id": "A", "text": "Immaculate and organized; everything has its dedicated place at all times"},
            {"id": "B", "text": "Generally clean and tidy with regular maintenance, tolerating minor mess"},
            {"id": "C", "text": "Relaxed and casual; clean up mainly when clutter becomes noticeable"},
            {"id": "D", "text": "Disorganized/chaotic; household chores are low priority and easily delayed"},
        ],
        "scores": {
            "A": {"lifestyle_preference": 5},
            "B": {"lifestyle_preference": 4},
            "C": {"lifestyle_preference": 2},
            "D": {"lifestyle_preference": 1},
        },
    },
    {
        "id": 38,
        "dimension": "lifestyle_preference",
        "dimension_name": "Lifestyle & Routine",
        "question": "Your sleep schedule and daily rhythm typically resemble:",
        "options": [
            {"id": "A", "text": "Consistent early riser (early to bed, structured morning routine every day)"},
            {"id": "B", "text": "Moderate regular schedule with occasional late weekend nights"},
            {"id": "C", "text": "Night owl with irregular sleep hours depending on work and mood"},
            {"id": "D", "text": "Completely unpredictable; sleep patterns fluctuate wildly day to day"},
        ],
        "scores": {
            "A": {"lifestyle_preference": 5},
            "B": {"lifestyle_preference": 4},
            "C": {"lifestyle_preference": 2},
            "D": {"lifestyle_preference": 1},
        },
    },
    {
        "id": 39,
        "dimension": "lifestyle_preference",
        "dimension_name": "Lifestyle & Routine",
        "question": "Physical fitness, nutrition, and healthy living habits play what role in your daily life?",
        "options": [
            {"id": "A", "text": "Disciplined daily non-negotiable; consistent workouts and clean nutrition"},
            {"id": "B", "text": "Important; regular exercise and mindful eating several days a week"},
            {"id": "C", "text": "Occasional spurts of exercise, but generally casual about health routines"},
            {"id": "D", "text": "Minimal attention paid to fitness or diet; comfort food and leisure rule"},
        ],
        "scores": {
            "A": {"lifestyle_preference": 5},
            "B": {"lifestyle_preference": 4},
            "C": {"lifestyle_preference": 2},
            "D": {"lifestyle_preference": 1},
        },
    },
    {
        "id": 40,
        "dimension": "lifestyle_preference",
        "dimension_name": "Lifestyle & Routine",
        "question": "How do you prefer sharing domestic chores and daily household management?",
        "options": [
            {"id": "A", "text": "Clear division of tasks or roster, executed reliably and cooperatively"},
            {"id": "B", "text": "Flexible partnership where both step in organically according to bandwidth"},
            {"id": "C", "text": "Tend to wait for reminders or requests before doing chores"},
            {"id": "D", "text": "Resent household tasks and prefer hiring help or letting chores slide"},
        ],
        "scores": {
            "A": {"lifestyle_preference": 5, "conflict_handling": 4},
            "B": {"lifestyle_preference": 4, "conflict_handling": 4},
            "C": {"lifestyle_preference": 2, "conflict_handling": 2},
            "D": {"lifestyle_preference": 1, "conflict_handling": 1},
        },
    },
]

# Helper lookup by question id
QUESTION_LOOKUP = {q["id"]: q for q in QUESTIONS}

def get_dimension_bounds():
    """Calculate minimum and maximum possible raw points achievable for each dimension."""
    min_scores = {dim: 0.0 for dim in DIMENSIONS}
    max_scores = {dim: 0.0 for dim in DIMENSIONS}
    for q in QUESTIONS:
        dim_options = {}
        for opt_id, scores_map in q["scores"].items():
            for dim, pts in scores_map.items():
                if dim not in dim_options:
                    dim_options[dim] = []
                dim_options[dim].append(pts)
        for dim, pts_list in dim_options.items():
            min_scores[dim] += min(pts_list)
            max_scores[dim] += max(pts_list)
    return min_scores, max_scores

MIN_POSSIBLE_SCORES, MAX_POSSIBLE_SCORES = get_dimension_bounds()
