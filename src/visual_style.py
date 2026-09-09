"""
Visual Style Configuration for Women's Boxing Films
Defines lighting, cinematography, color grading, and aesthetic preferences
"""

from enum import Enum
from typing import Dict, List
from pydantic import BaseModel

class LightingStyle(str, Enum):
    """Professional boxing lighting styles"""
    DRAMATIC_RING = "dramatic_ring"  # High contrast, dramatic shadows
    INTIMATE_CLOSE = "intimate_close"  # Warm, flattering close-up lighting
    ARENA_PROFESSIONAL = "arena_professional"  # Authentic arena lighting
    CINEMATIC_GOLDEN = "cinematic_golden"  # Golden hour warm tones
    MOODY_INTENSE = "moody_intense"  # Dark, intense dramatic lighting
    BRIGHT_ATHLETIC = "bright_athletic"  # Well-lit athletic showcase lighting

class ColorGrade(str, Enum):
    """Color grading styles"""
    WARM_GLAMOROUS = "warm_glamorous"  # Warm tones, flattering skin
    COOL_ATHLETIC = "cool_athletic"  # Cool tones, energetic feel
    VIBRANT_PROFESSIONAL = "vibrant_professional"  # Saturated, vivid colors
    CINEMATIC_NEUTRAL = "cinematic_neutral"  # Neutral, film-like
    HIGH_CONTRAST = "high_contrast"  # Bold contrast, striking visuals
    DESATURATED_MOODY = "desaturated_moody"  # Moody, dramatic desaturation

class CameraAngle(str, Enum):
    """Camera angle preferences"""
    LOW_ANGLE = "low_angle"  # Powerful, dominant perspective
    EYE_LEVEL = "eye_level"  # Intimate, direct connection
    CLOSE_UP = "close_up"  # Detailed facial/body detail
    WIDE_ATHLETIC = "wide_athletic"  # Full body athletic showcase
    OVERHEAD = "overhead"  # Ring perspective
    DYNAMIC_MULTIPLE = "dynamic_multiple"  # Mix of angles

class ClothingStyle(str, Enum):
    """Professional boxing attire options"""
    PROFESSIONAL_MODEST = "professional_modest"  # Standard boxing gear
    ATHLETIC_FITTED = "athletic_fitted"  # Form-fitting athletic wear
    SLEEK_MINIMAL = "sleek_minimal"  # Minimal, streamlined design
    STYLIZED_PROFESSIONAL = "stylized_professional"  # Fashion-forward but modest

class VisualStylePreset(BaseModel):
    """Pre-configured visual style for boxing films"""
    name: str
    lighting: LightingStyle
    color_grade: ColorGrade
    primary_camera_angles: List[CameraAngle]
    skin_texture_detail: str  # low, medium, high
    muscle_definition_emphasis: str  # subtle, moderate, prominent
    clothing_style: ClothingStyle
    makeup_level: str  # natural, enhanced, bold
    hair_style_detail: str  # Description of hair styling
    closeup_focus_areas: List[str]  # Facial expression, shoulders, core, arms, etc.
    description: str

# Pre-configured visual style presets
VISUAL_STYLE_PRESETS = {
    "athletic_professional": VisualStylePreset(
        name="Athletic Professional",
        lighting=LightingStyle.ARENA_PROFESSIONAL,
        color_grade=ColorGrade.VIBRANT_PROFESSIONAL,
        primary_camera_angles=[
            CameraAngle.DYNAMIC_MULTIPLE,
            CameraAngle.CLOSE_UP,
            CameraAngle.WIDE_ATHLETIC
        ],
        skin_texture_detail="high",
        muscle_definition_emphasis="prominent",
        clothing_style=ClothingStyle.PROFESSIONAL_MODEST,
        makeup_level="enhanced",
        hair_style_detail="Sleek, pulled back for movement, athletic styling",
        closeup_focus_areas=["facial_expression", "shoulders", "core", "footwork"],
        description="Professional arena setting with emphasis on athletic excellence and technical movement"
    ),
    
    "cinematic_glamorous": VisualStylePreset(
        name="Cinematic Glamorous",
        lighting=LightingStyle.CINEMATIC_GOLDEN,
        color_grade=ColorGrade.WARM_GLAMOROUS,
        primary_camera_angles=[
            CameraAngle.CLOSE_UP,
            CameraAngle.EYE_LEVEL,
            CameraAngle.LOW_ANGLE
        ],
        skin_texture_detail="high",
        muscle_definition_emphasis="prominent",
        clothing_style=ClothingStyle.ATHLETIC_FITTED,
        makeup_level="bold",
        hair_style_detail="Styled and flowing, with confident presence",
        closeup_focus_areas=["facial_expression", "eyes", "shoulders", "core_definition"],
        description="Cinematic glamorous style with warm golden lighting, emphasizing confidence and beauty alongside athleticism"
    ),
    
    "moody_intense": VisualStylePreset(
        name="Moody Intense",
        lighting=LightingStyle.MOODY_INTENSE,
        color_grade=ColorGrade.HIGH_CONTRAST,
        primary_camera_angles=[
            CameraAngle.CLOSE_UP,
            CameraAngle.DYNAMIC_MULTIPLE,
            CameraAngle.LOW_ANGLE
        ],
        skin_texture_detail="high",
        muscle_definition_emphasis="prominent",
        clothing_style=ClothingStyle.SLEEK_MINIMAL,
        makeup_level="enhanced",
        hair_style_detail="Sleek, defined lines, intense styling",
        closeup_focus_areas=["facial_expression", "intensity_in_eyes", "muscle_definition"],
        description="Dark, intense dramatic lighting with high contrast, emphasizing power and determination"
    ),
    
    "intimate_close": VisualStylePreset(
        name="Intimate Close",
        lighting=LightingStyle.INTIMATE_CLOSE,
        color_grade=ColorGrade.WARM_GLAMOROUS,
        primary_camera_angles=[
            CameraAngle.CLOSE_UP,
            CameraAngle.EYE_LEVEL
        ],
        skin_texture_detail="high",
        muscle_definition_emphasis="moderate",
        clothing_style=ClothingStyle.ATHLETIC_FITTED,
        makeup_level="enhanced",
        hair_style_detail="Softly styled, natural flow",
        closeup_focus_areas=["facial_expression", "eyes", "shoulders", "confidence"],
        description="Intimate, warm lighting focused on close-ups, emphasizing personality and connection"
    ),
    
    "bright_showcase": VisualStylePreset(
        name="Bright Showcase",
        lighting=LightingStyle.BRIGHT_ATHLETIC,
        color_grade=ColorGrade.VIBRANT_PROFESSIONAL,
        primary_camera_angles=[
            CameraAngle.WIDE_ATHLETIC,
            CameraAngle.CLOSE_UP,
            CameraAngle.DYNAMIC_MULTIPLE
        ],
        skin_texture_detail="high",
        muscle_definition_emphasis="prominent",
        clothing_style=ClothingStyle.PROFESSIONAL_MODEST,
        makeup_level="enhanced",
        hair_style_detail="Athletic styling, movement-ready",
        closeup_focus_areas=["athletic_form", "movement", "facial_determination"],
        description="Well-lit showcase of full athletic form with vibrant, energetic color grading"
    ),

    "stylized_sexy": VisualStylePreset(
        name="Stylized Sexy",
        lighting=LightingStyle.DRAMATIC_RING,
        color_grade=ColorGrade.WARM_GLAMOROUS,
        primary_camera_angles=[
            CameraAngle.CLOSE_UP,
            CameraAngle.LOW_ANGLE,
            CameraAngle.DYNAMIC_MULTIPLE
        ],
        skin_texture_detail="high",
        muscle_definition_emphasis="prominent",
        clothing_style=ClothingStyle.SLEEK_MINIMAL,
        makeup_level="bold",
        hair_style_detail="Styled for visual impact, confident presence",
        closeup_focus_areas=["facial_confidence", "athletic_form", "shoulders", "core_definition", "movement"],
        description="Stylized with dramatic lighting and strategic framing, emphasizing confidence, power, and visual appeal while maintaining professionalism"
    )
}

def get_visual_style_prompt(preset_name: str = "cinematic_glamorous") -> str:
    """
    Generate a detailed visual style prompt for video generation
    """
    if preset_name not in VISUAL_STYLE_PRESETS:
        preset_name = "cinematic_glamorous"
    
    preset = VISUAL_STYLE_PRESETS[preset_name]
    
    lighting_descriptions = {
        LightingStyle.DRAMATIC_RING: "Dramatic ring lighting with high contrast, emphasis on definition and form",
        LightingStyle.INTIMATE_CLOSE: "Warm, intimate lighting designed for close-ups, flattering and detailed",
        LightingStyle.ARENA_PROFESSIONAL: "Professional arena lighting that authentically showcases athletic movement",
        LightingStyle.CINEMATIC_GOLDEN: "Golden hour cinematic lighting with warm, flattering tones",
        LightingStyle.MOODY_INTENSE: "Dark, moody dramatic lighting emphasizing intensity and power",
        LightingStyle.BRIGHT_ATHLETIC: "Bright, well-lit athletic showcase lighting"
    }
    
    color_descriptions = {
        ColorGrade.WARM_GLAMOROUS: "Warm color grading with flattering skin tones, glamorous appeal",
        ColorGrade.COOL_ATHLETIC: "Cool color tones with energetic, athletic feel",
        ColorGrade.VIBRANT_PROFESSIONAL: "Vibrant, saturated professional colors with striking visual impact",
        ColorGrade.CINEMATIC_NEUTRAL: "Neutral cinematic color grading for film-like quality",
        ColorGrade.HIGH_CONTRAST: "Bold high-contrast color grading with striking visuals",
        ColorGrade.DESATURATED_MOODY: "Desaturated moody tones for dramatic effect"
    }
    
    prompt = f"""
VISUAL STYLE: {preset.name}

LIGHTING:
{lighting_descriptions.get(preset.lighting, str(preset.lighting))}

COLOR GRADING:
{color_descriptions.get(preset.color_grade, str(preset.color_grade))}

CAMERA DIRECTION:
Focus on {', '.join([angle.value for angle in preset.primary_camera_angles])} perspectives.

APPEARANCE & DETAIL:
- Skin texture: Highly detailed, clear skin with athletic glow
- Muscle definition: {preset.muscle_definition_emphasis.capitalize()} emphasis on athletic muscle tone
- Professional appearance with polished details
- Hair: {preset.hair_style_detail}
- Makeup: {preset.makeup_level.capitalize()} makeup that enhances facial features and confidence

CLOTHING:
{preset.clothing_style.value.replace('_', ' ').title()} - professional and athletic

CLOSE-UP FOCUS:
Primary focus on: {', '.join(preset.closeup_focus_areas)}

OVERALL AESTHETIC:
{preset.description}

COMPOSITION GOALS:
- Emphasize athletic excellence and confidence
- Frame to highlight fitness and strength
- Professional but visually striking presentation
- Tasteful and sophisticated throughout
- Dynamic movement and powerful presence
"""
    
    return prompt

def get_character_visual_description(character_data: Dict, visual_style: str = "cinematic_glamorous") -> str:
    """
    Generate detailed visual description of character based on data and style preference
    """
    preset = VISUAL_STYLE_PRESETS.get(visual_style, VISUAL_STYLE_PRESETS["cinematic_glamorous"])
    
    description = f"""
CHARACTER VISUAL PROFILE:

Name: {character_data.get('name', 'Boxer')}
Age: {character_data.get('age', 'N/A')}
Weight Class: {character_data.get('weight_class', 'N/A')}

PHYSICAL APPEARANCE:
{character_data.get('appearance', 'Athletic boxer physique')}
Muscle tone: Prominent definition reflecting professional boxing training
Fitness level: Elite athlete conditioning

VISUAL STYLING FOR VIDEO:
Makeup: {preset.makeup_level.capitalize()} - enhancing natural features and confidence
Hair: {preset.hair_style_detail}
Clothing: {preset.clothing_style.value.replace('_', ' ')}

CINEMATOGRAPHY DIRECTION:
- Lighting: {preset.lighting.value.replace('_', ' ').title()}
- Color Grade: {preset.color_grade.value.replace('_', ' ').title()}
- Primary Camera Angles: {', '.join([a.value.replace('_', ' ').title() for a in preset.primary_camera_angles])}

CHARACTER PRESENCE:
{character_data.get('personality', 'Confident and determined')}

VISUAL IMPACT:
- Emphasize: {', '.join(preset.closeup_focus_areas)}
- Convey: Confidence, athleticism, power, and professional excellence
- Maintain: Sophisticated, tasteful presentation

FIGHTING STYLE VISUALS:
{character_data.get('fighting_style', 'Technical and powerful')}
"""
    
    return description

# Export all presets as a lookup dictionary
ALL_STYLES = {name: preset.name for name, preset in VISUAL_STYLE_PRESETS.items()}
