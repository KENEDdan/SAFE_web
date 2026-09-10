from django.db import models

from apps.core.models import SingletonModel
from apps.core.validators import validate_image_extension, validate_image_size

IMG = dict(
    upload_to="pages/",
    blank=True,
    null=True,
    validators=[validate_image_extension, validate_image_size],
)


class HomePage(SingletonModel):
    hero_title = models.CharField(
        max_length=200,
        default="Cultivating Resilience, Growing Futures",
    )
    hero_subtitle = models.CharField(
        max_length=300,
        default=(
            "Empowering communities in South Sudan through sustainable agriculture, "
            "climate action, and environmental conservation for a resilient future."
        ),
    )
    hero_image = models.ImageField(**IMG)
    hero_cta_label = models.CharField(max_length=60, default="Get Involved")
    hero_cta_url = models.CharField(max_length=200, default="/get-involved/")
    hero_secondary_label = models.CharField(max_length=60, blank=True, default="Our Work")
    hero_secondary_url = models.CharField(max_length=200, blank=True, default="/what-we-do/")

    intro_heading = models.CharField(max_length=200, default="Who We Are")
    intro_body = models.TextField(
        default=(
            "SAFE is a non-governmental organization dedicated to building resilient "
            "communities through sustainable agriculture and environmental stewardship "
            "in South Sudan. We work at the intersection of agriculture, climate action, "
            "and community development, bringing together traditional knowledge and modern "
            "sustainable practices to create lasting impact."
        )
    )

    what_we_do_heading = models.CharField(max_length=200, default="What We Do")
    what_we_do_intro = models.CharField(
        max_length=300,
        default="Our comprehensive approach to sustainable development and community empowerment.",
    )

    impact_heading = models.CharField(max_length=200, default="Our Impact")
    impact_intro = models.CharField(
        max_length=300,
        default="Creating lasting change through sustainable development and community empowerment.",
    )

    projects_heading = models.CharField(max_length=200, default="Featured Projects")
    projects_intro = models.CharField(
        max_length=300,
        default="Showcasing our sustainable farming and community agriculture projects.",
    )

    gallery_heading = models.CharField(max_length=200, default="Agriculture in Action")
    gallery_intro = models.CharField(
        max_length=300, default="A visual journey through our work across South Sudan.",
    )

    testimonials_heading = models.CharField(max_length=200, default="Community Voices")
    testimonials_intro = models.CharField(
        max_length=300, default="Stories of transformation from the communities we serve.",
    )

    news_heading = models.CharField(max_length=200, default="Latest News & Updates")
    news_intro = models.CharField(
        max_length=300,
        default="Field stories, events, and publications from across our work.",
    )

    cta_heading = models.CharField(max_length=200, default="Join Us in Making a Difference")
    cta_body = models.TextField(
        default=(
            "Together, we can build resilient communities and create sustainable futures "
            "for South Sudan. Your support enables us to reach more families and protect "
            "our environment."
        )
    )
    cta_button_label = models.CharField(max_length=60, default="Get Involved Today")
    cta_button_url = models.CharField(max_length=200, default="/get-involved/")

    def __str__(self):
        return "Home page"


class AboutPage(SingletonModel):
    hero_title = models.CharField(max_length=200, default="About SAFE")
    hero_subtitle = models.CharField(
        max_length=300,
        default="Building resilient communities through sustainable agriculture and environmental stewardship.",
    )
    hero_image = models.ImageField(**IMG)

    director_name = models.CharField(max_length=150, default="Ayom Mawien Arou")
    director_role = models.CharField(max_length=150, default="Executive Director, SAFE")
    director_photo = models.ImageField(**IMG)
    director_message = models.TextField(
        default=(
            "It is with great pride and humility that I welcome you to SAFE - Sustainable "
            "Agriculture and Forest Environment. Our organization was born from a deep "
            "commitment to addressing the interconnected challenges of food insecurity, "
            "environmental degradation, and climate vulnerability facing communities across "
            "South Sudan.\n\n"
            "Through our work, we have witnessed the incredible resilience and determination "
            "of smallholder farmers who, despite facing numerous challenges, continue to "
            "nurture the land and feed their families. Our mission is to support these "
            "communities with the knowledge, resources, and partnerships they need to thrive "
            "sustainably.\n\n"
            "Together, we are cultivating not just crops, but hope, resilience, and a "
            "sustainable future for generations to come."
        )
    )

    story_heading = models.CharField(max_length=200, default="Our Story")
    story_body = models.TextField(
        default=(
            "SAFE was established in response to the urgent need for sustainable agricultural "
            "solutions in South Sudan. Our founders recognized that food security and "
            "environmental sustainability are inseparable, and that communities must be at the "
            "center of any meaningful change.\n\n"
            "We work with smallholder farmers to build resilient agricultural systems that "
            "ensure sustainable agriculture and forest environment while protecting the "
            "environment. Our approach combines traditional knowledge with modern sustainable "
            "practices to increase yields and improve livelihoods."
        )
    )

    mission = models.TextField(
        default=(
            "To empower smallholder farming communities through sustainable agricultural "
            "practices, climate action, and environmental conservation, fostering resilience "
            "and food security."
        )
    )
    vision = models.TextField(
        default=(
            "A South Sudan where communities thrive through sustainable agriculture, "
            "environmental stewardship, and climate resilience, ensuring food security and "
            "prosperity for all."
        )
    )

    values_heading = models.CharField(max_length=200, default="Our Values")
    values_intro = models.CharField(
        max_length=300,
        default="Guiding principles that shape our work and commitment to communities.",
    )

    team_heading = models.CharField(max_length=200, default="Our Team")
    team_intro = models.CharField(
        max_length=300, default="The people driving SAFE's mission across South Sudan.",
    )

    legal_profile_heading = models.CharField(max_length=200, default="Legal and Operational Profile")
    legal_profile = models.TextField(
        blank=True,
        default=(
            "SAFE is a registered non-governmental organization operating in South Sudan, "
            "with programmes in Warrap State, Northern Bahr el Ghazal State, and Central "
            "Equatoria. SAFE maintains a ZERO TOLERANCE policy for Sexual Exploitation, "
            "Abuse, and Harassment (SEAH)."
        ),
    )

    def __str__(self):
        return "About page"


class WhatWeDoPage(SingletonModel):
    hero_title = models.CharField(max_length=200, default="What We Do")
    hero_subtitle = models.CharField(
        max_length=300,
        default="Our comprehensive approach to sustainable development and community empowerment.",
    )
    hero_image = models.ImageField(**IMG)
    intro = models.TextField(
        default=(
            "We work with smallholder farmers to build resilient agricultural systems that "
            "ensure food security while protecting the environment. Our approach combines "
            "traditional knowledge with modern sustainable practices to increase yields and "
            "improve livelihoods."
        )
    )
    programs_heading = models.CharField(max_length=200, default="Our Programmes")
    approach_heading = models.CharField(max_length=200, default="Our Approach")
    approach_body = models.TextField(
        default=(
            "We work at the intersection of agriculture, climate action, and community "
            "development, bringing together traditional knowledge and modern sustainable "
            "practices to create lasting impact."
        )
    )
    themes_heading = models.CharField(max_length=200, default="Cross-Cutting Themes")
    themes_intro = models.TextField(
        default=(
            "Our cross-cutting themes ensure that all our interventions are inclusive, safe, "
            "and sensitive to the complex dynamics of the communities we serve. We integrate "
            "these principles across all our programmes to maximize positive impact and ensure "
            "sustainable outcomes."
        )
    )

    def __str__(self):
        return "What We Do page"


class ImpactPage(SingletonModel):
    hero_title = models.CharField(max_length=200, default="Our Impact")
    hero_subtitle = models.CharField(
        max_length=300,
        default=(
            "Discover SAFE's measurable impact on food security, sustainable agriculture "
            "adoption, and environmental conservation across communities."
        ),
    )
    hero_image = models.ImageField(**IMG)
    intro = models.TextField(
        default="Creating lasting change through sustainable development and community empowerment.",
    )
    stats_heading = models.CharField(max_length=200, default="By the Numbers")
    beneficiaries_heading = models.CharField(max_length=200, default="Target Beneficiaries")
    beneficiaries_intro = models.CharField(
        max_length=300, default="Reaching communities across South Sudan.",
    )
    pathway_heading = models.CharField(max_length=200, default="Our Pathway to Change")
    pathway_intro = models.CharField(
        max_length=300, default="Our pathway to sustainable impact and community transformation.",
    )
    voices_heading = models.CharField(max_length=200, default="Community Voices")
    voices_intro = models.CharField(
        max_length=300, default="Stories of transformation from the communities we serve.",
    )
    gallery_heading = models.CharField(max_length=200, default="Visualizing the Transformation")

    def __str__(self):
        return "Impact page"


class ResourcesPage(SingletonModel):
    hero_title = models.CharField(max_length=200, default="Community Resources")
    hero_subtitle = models.CharField(
        max_length=300,
        default=(
            "Access SAFE's community resources, agricultural tools, training materials, and "
            "support programmes for sustainable farming and food security."
        ),
    )
    hero_image = models.ImageField(**IMG)
    intro = models.TextField(
        default="Supporting local communities with free seeds, organic goods, and agricultural resources.",
    )
    program_heading = models.CharField(max_length=200, default="Our Resource Distribution Programme")
    program_body = models.TextField(
        default=(
            "SAFE is committed to supporting local communities with the resources they need to "
            "build sustainable agricultural practices. Our resource distribution programme "
            "provides:\n"
            "Climate-resilient seed varieties suited to local conditions\n"
            "Basic farming tools and equipment\n"
            "Farmer field school training and materials\n"
            "Ongoing technical support and mentoring"
        )
    )
    catalogue_heading = models.CharField(max_length=200, default="Approved Resources Available")
    how_to_access_heading = models.CharField(max_length=200, default="How to Access Resources")
    how_to_access_body = models.TextField(
        default=(
            "To request resources for your community, please fill out the form below. Our team "
            "will review your request and contact you to arrange distribution and provide any "
            "necessary training."
        )
    )
    request_form_heading = models.CharField(max_length=200, default="Request Community Resources")
    request_form_intro = models.CharField(
        max_length=300,
        default="Tell us what your community needs and our team will be in touch.",
    )

    def __str__(self):
        return "Resources page"


class GetInvolvedPage(SingletonModel):
    hero_title = models.CharField(max_length=200, default="Get Involved")
    hero_subtitle = models.CharField(
        max_length=300,
        default="Join us in making a difference through donations, partnerships, or volunteering.",
    )
    hero_image = models.ImageField(**IMG)
    intro = models.TextField(
        default=(
            "Together, we can build resilient communities and create sustainable futures for "
            "South Sudan. Your support enables us to reach more families and protect our "
            "environment."
        )
    )

    donate_heading = models.CharField(max_length=200, default="Donate")
    donate_body = models.TextField(
        default=(
            "Your donation helps us provide seeds, tools, training, and support to farming "
            "communities across South Sudan. Every contribution makes a real difference in "
            "building sustainable livelihoods."
        )
    )

    volunteer_heading = models.CharField(max_length=200, default="Volunteer")
    volunteer_body = models.TextField(
        default=(
            "SAFE welcomes volunteers who are passionate about sustainable agriculture, "
            "environmental conservation, and community development. Whether you have technical "
            "expertise or simply want to contribute your time and energy, there are many ways "
            "to get involved.\n\n"
            "Send us a note with your background, skills, and areas of interest, and we'll get "
            "back to you with opportunities that match your profile."
        )
    )

    partner_heading = models.CharField(max_length=200, default="Partner With Us")
    partner_body = models.TextField(
        default=(
            "We welcome partnerships with organizations, businesses, and institutions that "
            "share our commitment to sustainable development. Together, we can amplify our "
            "impact and create lasting change."
        )
    )

    community_heading = models.CharField(max_length=200, default="Join Our Community")
    community_body = models.TextField(
        default=(
            "Connect with like-minded individuals passionate about environmental conservation "
            "and community resilience. Subscribe to our newsletter for the latest updates on "
            "sustainable agriculture, forest conservation, and community empowerment."
        )
    )

    def __str__(self):
        return "Get Involved page"
