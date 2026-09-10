"""Registry of console-managed content collections.

Projects are handled separately (slug URLs + an inline image gallery), so they
are not in this list.
"""

from . import forms, models
from .managecrud import Collection

COLLECTIONS = [
    Collection(
        key="programs", verbose="Programme", verbose_plural="Programmes",
        model=models.Program, form=forms.ProgramForm,
        columns=(("Title", "title"), ("Summary", "summary"), ("Published", "is_published")),
    ),
    Collection(
        key="themes", verbose="Cross-cutting theme", verbose_plural="Cross-cutting themes",
        model=models.CrossCuttingTheme, form=forms.CrossCuttingThemeForm,
        columns=(("Title", "title"), ("Published", "is_published")),
    ),
    Collection(
        key="values", verbose="Core value", verbose_plural="Core values",
        model=models.CoreValue, form=forms.CoreValueForm,
        columns=(("Title", "title"), ("Published", "is_published")),
    ),
    Collection(
        key="team", verbose="Team member", verbose_plural="Team & leadership",
        model=models.TeamMember, form=forms.TeamMemberForm,
        columns=(("Name", "name"), ("Role", "role"), ("Leadership", "is_leadership"), ("Published", "is_published")),
    ),
    Collection(
        key="partners", verbose="Partner", verbose_plural="Partners",
        model=models.Partner, form=forms.PartnerForm,
        columns=(("Name", "name"), ("Partnering on", "partnering_on"), ("Published", "is_published")),
    ),
    Collection(
        key="stats", verbose="Impact statistic", verbose_plural="Impact statistics",
        model=models.ImpactStat, form=forms.ImpactStatForm,
        columns=(("Value", "value"), ("Label", "label"), ("Published", "is_published")),
    ),
    Collection(
        key="beneficiaries", verbose="Target beneficiary", verbose_plural="Target beneficiaries",
        model=models.TargetBeneficiary, form=forms.TargetBeneficiaryForm,
        columns=(("Value", "value"), ("Label", "label"), ("Published", "is_published")),
    ),
    Collection(
        key="milestones", verbose="Milestone", verbose_plural="Pathway milestones",
        model=models.Milestone, form=forms.MilestoneForm,
        columns=(("Title", "title"), ("Period", "period"), ("Published", "is_published")),
    ),
    Collection(
        key="testimonials", verbose="Testimonial", verbose_plural="Testimonials",
        model=models.Testimonial, form=forms.TestimonialForm,
        columns=(("Author", "author"), ("Role", "role"), ("Featured", "is_featured"), ("Published", "is_published")),
    ),
    Collection(
        key="gallery", verbose="Gallery image", verbose_plural="Gallery images",
        model=models.GalleryImage, form=forms.GalleryImageForm,
        columns=(("Caption", "caption"), ("Category", "category"), ("Published", "is_published")),
    ),
    Collection(
        key="resources", verbose="Resource", verbose_plural="Resource catalogue",
        model=models.Resource, form=forms.ResourceForm,
        columns=(("Name", "name"), ("Category", "category"), ("Availability", "get_availability_display"), ("Published", "is_published")),
    ),
]

COLLECTIONS_BY_KEY = {c.key: c for c in COLLECTIONS}
