"""Populate the SAFE site with its launch content.

Idempotent: singletons are left at their model defaults (already the real
copy), and each collection is only seeded when it is empty. Seed images in
``static/images/seed/`` are copied into media on first run.
"""

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from apps.content import models as c
from apps.core.models import OrganizationProfile, SiteSettings
from apps.newsfeed.models import NewsCategory, NewsPost
from apps.pages import models as p
from apps.submissions.models import DonationSettings

SEED_DIR = Path(settings.BASE_DIR) / "static" / "images" / "seed"


def _img(name):
    path = SEED_DIR / name
    return File(path.open("rb"), name=name) if path.exists() else None


class Command(BaseCommand):
    help = "Seed the SAFE site with launch content."

    def handle(self, *args, **options):
        self._singletons()
        self._programs()
        self._themes()
        self._values()
        self._team()
        self._stats()
        self._beneficiaries()
        self._milestones()
        self._testimonials()
        self._gallery()
        self._resources()
        self._partners()
        self._projects()
        self._activities()
        self._news()
        self._org()
        self.stdout.write(self.style.SUCCESS("SAFE content seeded."))

    # ------------------------------------------------------------------
    def _singletons(self):
        site = SiteSettings.get_solo()
        if not site.logo:
            logo = _img("logo.png")
            if logo:
                site.logo.save("logo.png", logo, save=False)
        site.save()

        home = p.HomePage.get_solo()
        if not home.hero_image:
            hero = _img("hero.jpg")
            if hero:
                home.hero_image.save("hero.jpg", hero, save=False)
        home.save()

        for model in (p.AboutPage, p.WhatWeDoPage, p.ImpactPage, p.ResourcesPage, p.GetInvolvedPage):
            model.get_solo().save()

        about = p.AboutPage.get_solo()
        if not about.director_photo:
            photo = _img("photo-02.jpg")
            if photo:
                about.director_photo.save("director.jpg", photo, save=True)

        DonationSettings.get_solo().save()

    # ------------------------------------------------------------------
    def _seed(self, model, rows, image_field=None):
        if model.objects.exists():
            return
        for order, row in enumerate(rows):
            img_name = row.pop("_image", None)
            obj = model(display_order=order, **row)
            if image_field and img_name:
                f = _img(img_name)
                if f:
                    getattr(obj, image_field).save(img_name, f, save=False)
            obj.save()

    def _programs(self):
        self._seed(c.Program, [
            dict(title="Climate-Smart Crop Production", icon="🌾",
                 summary="Drought-resistant varieties, crop diversification, and sustainable techniques.",
                 description="Promoting drought-resistant varieties, crop diversification, and sustainable farming techniques that adapt to changing climate conditions."),
            dict(title="Agroforestry and Soil Health", icon="🌳",
                 summary="Integrating trees with crops to restore soil and add income.",
                 description="Integrating trees with crops to improve soil fertility, prevent erosion, and enhance biodiversity while providing additional income sources."),
            dict(title="Water Access & Irrigation", icon="💧",
                 summary="Rainwater harvesting and irrigation for reliable water access.",
                 description="Implementing rainwater harvesting, irrigation systems, and water conservation practices to ensure reliable water access for agriculture."),
            dict(title="Forest and Landscape Restoration", icon="🌲",
                 summary="Reforestation, natural regeneration, and community-led conservation.",
                 description="Restoring degraded lands through reforestation, natural regeneration, and community-led conservation initiatives."),
            dict(title="Post-Harvest Management & Market Linkages", icon="📦",
                 summary="Better storage, processing, and market access to raise incomes.",
                 description="Reducing food loss through improved storage, processing, and market linkages that increase farmer incomes and food availability."),
            dict(title="Community-Based Natural Resource Management", icon="🤝",
                 summary="Sustainable, community-led management of forests, water, and land.",
                 description="Strengthening community-based natural resource management and promoting sustainable use of forests, water, and land."),
        ], image_field="image")

    def _themes(self):
        self._seed(c.CrossCuttingTheme, [
            dict(title="Gender Equality and Social Inclusion (GESI)",
                 description="We actively promote equal opportunities and rights for all genders, recognizing the critical role of women in agriculture and community development. The SAFE-Her Harvest Initiative prioritizes women and youth in leadership and income-generation activities."),
            dict(title="Climate and Conflict Sensitivity",
                 description="Addressing the nexus of climate change and conflict, ensuring our interventions promote peace and do not exacerbate tensions."),
            dict(title="Safeguarding (Zero Tolerance for SEAH)",
                 description="SAFE maintains a ZERO TOLERANCE policy for Sexual Exploitation, Abuse, and Harassment, with continuous community awareness and sensitization on safeguarding mechanisms."),
            dict(title="Ecosystem-Based Adaptation",
                 description="Leveraging natural ecosystems to build resilience against climate impacts and protect communities from environmental hazards."),
            dict(title="Adaptive Learning",
                 description="We embrace continuous learning, innovation, and adaptation based on evidence, feedback, and changing contexts."),
        ])

    def _values(self):
        self._seed(c.CoreValue, [
            dict(title="Integrity & Accountability", icon="⚖️",
                 description="We maintain the highest standards of transparency, ethical conduct, and accountability to our stakeholders and beneficiaries."),
            dict(title="Community First", icon="🤝",
                 description="We prioritize the needs, voices, and agency of the communities we serve, ensuring they lead their own development journeys."),
            dict(title="Ecological Integrity", icon="🌍",
                 description="We are committed to protecting and restoring natural ecosystems, promoting biodiversity, and ensuring sustainable use of resources."),
            dict(title="Conflict Sensitivity", icon="🕊️",
                 description="We understand the complex dynamics of conflict and work to ensure our interventions contribute to peace and do not exacerbate tensions."),
            dict(title="Gender Equity", icon="♀️",
                 description="We promote equal opportunities and rights for all genders, recognizing the critical role of women in agriculture and community development."),
            dict(title="Continuous Improvement", icon="📈",
                 description="We embrace continuous learning, innovation, and adaptation based on evidence, feedback, and changing contexts."),
        ])

    def _team(self):
        self._seed(c.TeamMember, [
            dict(name="Ayom Mawien Arou", role="Executive Director", is_leadership=True,
                 email="ayom.mawien@safe-ss.org",
                 qualifications="Agricultural development & climate resilience",
                 bio="Ayom leads SAFE's mission to build climate-resilient farming communities across South Sudan."),
            dict(name="Programme Manager", role="Programme Manager", is_leadership=True,
                 qualifications="Sustainable agriculture & M&E",
                 bio="Oversees SAFE's field programmes, partnerships, and monitoring across Warrap and Northern Bahr el Ghazal."),
            dict(name="Field Coordinator", role="Field Coordinator — Warrap",
                 qualifications="Agronomy",
                 bio="Coordinates farmer field schools and input distribution with community structures."),
            dict(name="GESI & Safeguarding Officer", role="GESI & Safeguarding Officer",
                 bio="Leads the SAFE-Her Harvest Initiative and safeguarding across all activities."),
            dict(name="Finance & Operations Officer", role="Finance & Operations Officer",
                 bio="Manages grants, procurement, and day-to-day operations."),
        ], image_field="photo")

    def _partners(self):
        self._seed(c.Partner, [
            dict(name="Local government partners", partnering_on="Coordination and community mobilization",
                 blurb="State and county authorities in Warrap and Northern Bahr el Ghazal."),
            dict(name="Community-based organizations", partnering_on="Farmer field schools and distribution",
                 blurb="Grassroots partners that co-deliver training and reach farming households."),
            dict(name="Development donors", partnering_on="Programme funding",
                 blurb="Institutional funders supporting climate-smart agriculture and food security."),
        ], image_field="logo")

    def _stats(self):
        self._seed(c.ImpactStat, [
            dict(value="5,000", label="Households Reached", icon="🏠"),
            dict(value="30,000", label="Individuals Impacted", icon="👥"),
            dict(value="3 Years", label="Target Timeline", icon="📅"),
        ])

    def _beneficiaries(self):
        self._seed(c.TargetBeneficiary, [
            dict(value="5,000", label="Smallholder Farming Households"),
            dict(value="Warrap & NBeG", label="Warrap State and Northern Bahr el Ghazal State"),
            dict(value="Central Equatoria", label="Juba and surrounding communities"),
        ])

    def _milestones(self):
        self._seed(c.Milestone, [
            dict(period="Inputs", title="Improved farming practices",
                 description="Climate-resilient seeds, tools, and farmer field school training reach communities."),
            dict(period="Outputs", title="Increased yields & restored ecosystems",
                 description="Farmers adopt sustainable techniques; degraded land is brought back into production."),
            dict(period="Outcomes", title="Food security & climate resilience",
                 description="Households achieve reliable food supply and sustainable livelihoods."),
            dict(period="Impact", title="Thriving, resilient communities",
                 description="Communities thrive through sustainable agriculture, environmental stewardship, and lasting prosperity."),
        ])

    def _testimonials(self):
        self._seed(c.Testimonial, [
            dict(author="Nyandeng", role="Farmer", location="Warrap State", is_featured=True,
                 story="The drought-resistant seeds and training from SAFE changed how we farm. This season we harvested enough to feed our family and sell at the market."),
            dict(author="James", role="Community leader", location="Northern Bahr el Ghazal", is_featured=True,
                 story="SAFE brought us together to manage our land and water. Our trees are growing back and the soil is healthier."),
            dict(author="Aluel", role="Women's group chair", location="Central Equatoria", is_featured=True,
                 story="Through the SAFE-Her Harvest Initiative, women in our village now lead the vegetable gardens and earn our own income."),
        ], image_field="photo")

    def _gallery(self):
        if c.GalleryImage.objects.exists():
            return
        captions = [
            "Farmers harvesting sustainable crops in South Sudan",
            "Farmer field school demonstration of new techniques",
            "Agroforestry training session for farmers",
            "Community members working together in the field",
            "Women farmers leading community agricultural initiatives",
            "Water storage tanks for community irrigation",
            "Climate-resilient seed varieties distributed to communities",
            "Large community group engaged in sustainable farming",
        ]
        for i, caption in enumerate(captions):
            f = _img(f"photo-{i + 3:02d}.jpg")
            if not f:
                continue
            obj = c.GalleryImage(display_order=i, caption=caption, category="Field work")
            obj.image.save(f"gallery-{i + 1}.jpg", f, save=True)

    def _resources(self):
        self._seed(c.Resource, [
            dict(name="Climate-resilient seeds", category="Seeds",
                 description="Drought-resistant seed varieties suited to local conditions."),
            dict(name="Basic farming tools", category="Tools",
                 description="Hand tools and equipment for land preparation and planting."),
            dict(name="Farmer field school training", category="Training",
                 description="Practical, climate-smart farming techniques and ongoing mentoring."),
            dict(name="Agroforestry seedlings", category="Seedlings",
                 description="Tree seedlings for integration with crops and land restoration."),
        ], image_field="image")

    def _projects(self):
        if c.Project.objects.exists():
            return
        proj = c.Project(
            title="Climate-Smart Agriculture Initiative",
            location="Warrap State",
            status=c.ProjectStatus.ONGOING,
            is_featured=True,
            display_order=0,
            summary="Introducing drought-resistant crops and sustainable farming techniques across Warrap State.",
            body=(
                "SAFE works with smallholder farming households in Warrap State to build "
                "resilient agricultural systems. The initiative combines climate-resilient "
                "seed distribution, farmer field schools, agroforestry, and water access "
                "improvements to raise yields while restoring the environment."
            ),
            outcomes=(
                "Improved farming practices and higher yields\n"
                "Restored and protected local ecosystems\n"
                "Stronger food security for participating households\n"
                "Women and youth leading income-generation activities"
            ),
        )
        f = _img("photo-01.jpg")
        if f:
            proj.thumbnail.save("climate-smart.jpg", f, save=False)
        proj.save()
        for i in range(2, 5):
            gi = _img(f"photo-{i:02d}.jpg")
            if gi:
                c.ProjectImage.objects.create(project=proj, image=File(gi, name=f"cs-{i}.jpg"), display_order=i)

    def _news(self):
        if NewsPost.objects.exists():
            return
        rows = [
            dict(
                category=NewsCategory.FIELD_STORY,
                title="Farmer field schools reach 20 communities in Warrap",
                brief_description="Smallholder farmers are adopting drought-resistant seed and conservation techniques through hands-on training.",
                body=(
                    "Over the past season, SAFE's farmer field schools brought practical, "
                    "climate-smart training to twenty communities across Warrap State.\n\n"
                    "Participating households received drought-resistant seed varieties and "
                    "learned soil and water conservation techniques they can apply on their "
                    "own plots. Early results show improved germination rates and stronger "
                    "yields even in a difficult rainfall year.\n\n"
                    "The programme continues to expand, with women and youth prioritised for "
                    "leadership roles through the SAFE-Her Harvest Initiative."
                ),
                _image="photo-05.jpg",
            ),
            dict(
                category=NewsCategory.EVENT,
                title="Community tree-planting day marks the start of the rains",
                brief_description="Hundreds of seedlings went into the ground as communities kicked off this year's landscape restoration work.",
                body=(
                    "SAFE joined community members, local leaders, and school groups for a "
                    "tree-planting day at the start of the rainy season.\n\n"
                    "The event is part of SAFE's forest and landscape restoration programme, "
                    "which pairs reforestation with community-led natural resource management "
                    "so that the new trees are protected and maintained over time."
                ),
                _image="photo-06.jpg",
            ),
            dict(
                category=NewsCategory.UPDATE,
                title="SAFE-Her Harvest Initiative launches women-led vegetable gardens",
                brief_description="New income-generation activity puts women and youth at the centre of community agriculture.",
                body=(
                    "The SAFE-Her Harvest Initiative has launched its first women-led "
                    "vegetable gardens, giving participants a reliable source of nutrition "
                    "and income.\n\n"
                    "Groups manage the gardens collectively, reinvesting proceeds into seed, "
                    "tools, and training for the next planting cycle."
                ),
                _image="photo-07.jpg",
            ),
        ]
        for row in rows:
            img_name = row.pop("_image", None)
            post = NewsPost(**row)
            f = _img(img_name) if img_name else None
            if f:
                post.thumbnail.save(img_name, f, save=False)
            post.save()

    def _activities(self):
        if c.Activity.objects.exists():
            return
        rows = [
            dict(
                category=c.ActivityCategory.TRAINING,
                title="Farmer field school on climate-smart techniques",
                location="Warrap State",
                sponsors="SAFE, community-based organizations",
                summary="Hands-on training in drought-resistant seed, spacing, and soil and water conservation.",
                body=(
                    "Farmers gathered at demonstration plots to practise climate-smart "
                    "techniques they can take back to their own fields. Sessions covered "
                    "seed selection, planting density, mulching, and simple water "
                    "harvesting."
                ),
                _image="photo-08.jpg",
            ),
            dict(
                category=c.ActivityCategory.DISTRIBUTION,
                title="Seed and tool distribution ahead of the planting season",
                location="Northern Bahr el Ghazal State",
                sponsors="SAFE, local government partners",
                summary="Climate-resilient seed varieties and basic tools reached farming households before the rains.",
                body=(
                    "Working with community structures, SAFE distributed drought-resistant "
                    "seed and hand tools to households, paired with a short orientation on "
                    "getting the most from the inputs."
                ),
                _image="photo-09.jpg",
            ),
            dict(
                category=c.ActivityCategory.DIALOGUE,
                title="Community dialogue on natural resource management",
                location="Central Equatoria",
                summary="Communities agreed shared rules for managing forests, grazing land, and water points.",
                body=(
                    "The dialogue brought together farmers, women's groups, and local "
                    "leaders to talk through pressures on shared resources and agree "
                    "conflict-sensitive ways to manage them together."
                ),
                _image="photo-10.jpg",
            ),
        ]
        for order, row in enumerate(rows):
            img_name = row.pop("_image", None)
            act = c.Activity(display_order=order, **row)
            f = _img(img_name) if img_name else None
            if f:
                act.thumbnail.save(img_name, f, save=False)
            act.save()

    def _org(self):
        org = OrganizationProfile.get_solo()
        if not org.communities_served:
            org.field_staff_count = 8
            org.volunteers_count = 40
            org.communities_served = 20
            org.states_covered = 3
            org.partners_count = c.Partner.objects.count()
            org.years_active = 3
            org.auto_staff_count = True
            org.save()
