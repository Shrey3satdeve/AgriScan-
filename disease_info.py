"""
AgriScan - Crop Disease Detection
Disease metadata: treatment recommendations, severity levels, and affected crops.
"""

DISEASE_INFO = {
    # ── Apple ──────────────────────────────────────────────────────────────────
    "Apple___Apple_scab": {
        "display_name": "Apple Scab",
        "crop": "Apple",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "A fungal disease caused by Venturia inaequalis that creates dark, scabby lesions on leaves, fruits, and stems.",
        "symptoms": ["Dark, olive-green to black scabby spots on leaves", "Velvety texture on lesions", "Distorted or cracked fruit", "Premature leaf drop"],
        "treatment": ["Apply fungicide sprays (captan, myclobutanil) at 7-10 day intervals", "Remove and destroy infected plant material", "Improve air circulation by pruning", "Avoid overhead irrigation"],
        "prevention": ["Plant scab-resistant apple varieties", "Apply dormant oil spray before bud break", "Maintain proper tree spacing"]
    },
    "Apple___Black_rot": {
        "display_name": "Apple Black Rot",
        "crop": "Apple",
        "severity": "Severe",
        "severity_color": "#e74c3c",
        "description": "Caused by Botryosphaeria obtusa, it affects fruit, leaves, and bark causing rotting and cankers.",
        "symptoms": ["Brown to black lesions on fruit", "Concentric rings on rotting fruit", "'Frogeye' leaf spots with purple borders", "Cankers on branches"],
        "treatment": ["Remove all mummified fruit from the tree", "Prune out dead/cankered wood", "Apply captan or thiophanate-methyl fungicide", "Dispose of prunings away from orchard"],
        "prevention": ["Maintain tree vigor with proper fertilization", "Avoid wounding trees", "Control insects that create entry wounds"]
    },
    "Apple___Cedar_apple_rust": {
        "display_name": "Cedar Apple Rust",
        "crop": "Apple",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "A fungal disease requiring two hosts (apple and red cedar/juniper) to complete its life cycle.",
        "symptoms": ["Bright orange-yellow spots on upper leaf surface", "Tube-like structures on leaf undersides", "Distorted, dropping fruit", "Lesions on fruit and twigs"],
        "treatment": ["Apply fungicide (myclobutanil, trifloxystrobin) when orange spots appear", "Remove nearby juniper/cedar trees if possible", "Begin sprays at pink bud stage"],
        "prevention": ["Plant rust-resistant apple varieties", "Remove galls from cedar trees in late winter"]
    },
    "Apple___healthy": {
        "display_name": "Healthy Apple",
        "crop": "Apple",
        "severity": "None",
        "severity_color": "#27ae60",
        "description": "The apple plant appears healthy with no visible signs of disease.",
        "symptoms": ["No disease symptoms detected"],
        "treatment": ["No treatment needed"],
        "prevention": ["Continue regular monitoring", "Maintain proper fertilization and watering", "Practice good orchard hygiene"]
    },
    # ── Blueberry ──────────────────────────────────────────────────────────────
    "Blueberry___healthy": {
        "display_name": "Healthy Blueberry",
        "crop": "Blueberry",
        "severity": "None",
        "severity_color": "#27ae60",
        "description": "The blueberry plant appears healthy.",
        "symptoms": ["No disease symptoms detected"],
        "treatment": ["No treatment needed"],
        "prevention": ["Maintain acidic soil pH (4.5-5.5)", "Regular monitoring for pests"]
    },
    # ── Cherry ─────────────────────────────────────────────────────────────────
    "Cherry_(including_sour)___Powdery_mildew": {
        "display_name": "Cherry Powdery Mildew",
        "crop": "Cherry",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "Caused by Podosphaera clandestina, it creates a white powdery coating on cherry leaves and shoots.",
        "symptoms": ["White powdery coating on leaves", "Distorted, stunted new growth", "Leaves curl upward", "Early defoliation in severe cases"],
        "treatment": ["Apply sulfur-based or potassium bicarbonate fungicide", "Use neem oil as an organic option", "Remove heavily infected shoots"],
        "prevention": ["Maintain good air circulation", "Avoid excessive nitrogen fertilization", "Water at the base of the plant"]
    },
    "Cherry_(including_sour)___healthy": {
        "display_name": "Healthy Cherry",
        "crop": "Cherry",
        "severity": "None",
        "severity_color": "#27ae60",
        "description": "The cherry plant appears healthy.",
        "symptoms": ["No disease symptoms detected"],
        "treatment": ["No treatment needed"],
        "prevention": ["Regular monitoring", "Proper pruning for air circulation"]
    },
    # ── Corn (Maize) ───────────────────────────────────────────────────────────
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "display_name": "Corn Gray Leaf Spot",
        "crop": "Corn (Maize)",
        "severity": "Severe",
        "severity_color": "#e74c3c",
        "description": "A fungal disease caused by Cercospora zeae-maydis that can cause significant yield loss.",
        "symptoms": ["Rectangular, grayish-tan lesions on leaves", "Lesions follow leaf veins", "Brown, necrotic tissue in center", "Premature plant death in severe cases"],
        "treatment": ["Apply fungicide (strobilurins, triazoles) at early signs", "Choose resistant hybrids for future planting", "Crop rotation with non-host plants"],
        "prevention": ["Use disease-resistant corn hybrids", "Rotate crops annually", "Manage crop residue by tillage"]
    },
    "Corn_(maize)___Common_rust_": {
        "display_name": "Corn Common Rust",
        "crop": "Corn (Maize)",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "Caused by Puccinia sorghi, common rust produces brick-red pustules on corn leaves.",
        "symptoms": ["Oval, brick-red pustules on both leaf surfaces", "Pustules turn black late in season", "Yellow halos around pustules", "Reduced photosynthesis"],
        "treatment": ["Apply triazole or strobilurin fungicide if severe", "Evaluate economic threshold before spraying", "Remove heavily infected plants"],
        "prevention": ["Plant rust-resistant corn hybrids", "Early planting to avoid peak rust pressure"]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "display_name": "Corn Northern Leaf Blight",
        "crop": "Corn (Maize)",
        "severity": "Severe",
        "severity_color": "#e74c3c",
        "description": "Caused by Exserohilum turcicum, NLB produces cigar-shaped lesions that can devastate corn yields.",
        "symptoms": ["Long, cigar-shaped gray-green lesions", "Lesions 1-6 inches long", "Tan to gray center with dark borders", "Heavy sporulation gives lesions a dark appearance"],
        "treatment": ["Apply fungicide (azoxystrobin, propiconazole) at tasseling", "Start sprays before lesions reach upper leaves", "Remove and destroy infected plant material"],
        "prevention": ["Plant resistant hybrids", "Crop rotation", "Manage surface crop residue"]
    },
    "Corn_(maize)___healthy": {
        "display_name": "Healthy Corn",
        "crop": "Corn (Maize)",
        "severity": "None",
        "severity_color": "#27ae60",
        "description": "The corn plant appears healthy.",
        "symptoms": ["No disease symptoms detected"],
        "treatment": ["No treatment needed"],
        "prevention": ["Monitor regularly", "Balanced soil nutrition", "Proper irrigation management"]
    },
    # ── Grape ──────────────────────────────────────────────────────────────────
    "Grape___Black_rot": {
        "display_name": "Grape Black Rot",
        "crop": "Grape",
        "severity": "Severe",
        "severity_color": "#e74c3c",
        "description": "Caused by Guignardia bidwellii, black rot can destroy entire grape clusters if uncontrolled.",
        "symptoms": ["Tan lesions with dark borders on leaves", "Circular, brown rotted spots on berries", "Berries shrivel into hard, black 'mummies'", "Brown lesions on shoots and tendrils"],
        "treatment": ["Apply mancozeb or myclobutanil at pre-bloom, bloom, and post-bloom", "Remove mummified berries from vines and ground", "Ensure good canopy management"],
        "prevention": ["Remove all mummies before spring", "Maintain open canopy for air movement", "Avoid overhead irrigation"]
    },
    "Grape___Esca_(Black_Measles)": {
        "display_name": "Grape Esca (Black Measles)",
        "crop": "Grape",
        "severity": "Severe",
        "severity_color": "#e74c3c",
        "description": "A complex fungal disease causing tiger-stripe leaf symptoms and internal wood decay.",
        "symptoms": ["Interveinal chlorosis and necrosis creating tiger-stripe pattern", "Berries develop dark spotting", "Sudden wilting and death of shoots", "Internal wood discoloration"],
        "treatment": ["No effective chemical control exists once infected", "Remove and destroy infected vines", "Apply wound sealant after pruning", "Sodium arsenite was used historically (now banned)"],
        "prevention": ["Use clean planting material", "Seal all pruning wounds immediately", "Avoid large pruning cuts"]
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "display_name": "Grape Leaf Blight",
        "crop": "Grape",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "Caused by Isariopsis clavispora, it creates dark lesions leading to premature defoliation.",
        "symptoms": ["Dark brown irregular spots on leaves", "Lesions may coalesce covering large leaf areas", "Premature yellowing and leaf drop", "Reduced fruit quality"],
        "treatment": ["Apply copper-based fungicide or mancozeb", "Improve air circulation within canopy", "Remove infected leaves"],
        "prevention": ["Maintain proper vine spacing", "Avoid excessive nitrogen"]
    },
    "Grape___healthy": {
        "display_name": "Healthy Grape",
        "crop": "Grape",
        "severity": "None",
        "severity_color": "#27ae60",
        "description": "The grapevine appears healthy.",
        "symptoms": ["No disease symptoms detected"],
        "treatment": ["No treatment needed"],
        "prevention": ["Regular scouting", "Proper canopy management", "Balanced fertilization"]
    },
    # ── Orange ─────────────────────────────────────────────────────────────────
    "Orange___Haunglongbing_(Citrus_greening)": {
        "display_name": "Citrus Greening (HLB)",
        "crop": "Orange",
        "severity": "Critical",
        "severity_color": "#8e44ad",
        "description": "The most destructive citrus disease worldwide, caused by Candidatus Liberibacter spp., spread by the Asian citrus psyllid.",
        "symptoms": ["Asymmetric, blotchy yellowing of leaves (huanglongbing = yellow dragon disease)", "Small, lopsided, bitter fruit", "Green, aborted seeds", "Twig dieback and tree decline"],
        "treatment": ["No cure exists — infected trees must be removed", "Control psyllid vector with insecticides", "Trunk injection with oxytetracycline can suppress symptoms temporarily"],
        "prevention": ["Use certified disease-free planting material", "Control the Asian citrus psyllid aggressively", "Quarantine infected areas"]
    },
    # ── Peach ──────────────────────────────────────────────────────────────────
    "Peach___Bacterial_spot": {
        "display_name": "Peach Bacterial Spot",
        "crop": "Peach",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "Caused by Xanthomonas campestris pv. pruni, it affects leaves, fruit, and twigs.",
        "symptoms": ["Water-soaked spots on leaves that turn brown", "Leaf shothole appearance as centers fall out", "Sunken, dark spots on fruit", "Gummy cankers on twigs"],
        "treatment": ["Apply copper-based bactericide throughout the season", "Apply oxytetracycline (Mycoshield) during bloom", "Remove cankered wood during dry conditions"],
        "prevention": ["Plant resistant varieties", "Avoid overhead irrigation", "Maintain tree vigor"]
    },
    "Peach___healthy": {
        "display_name": "Healthy Peach",
        "crop": "Peach",
        "severity": "None",
        "severity_color": "#27ae60",
        "description": "The peach tree appears healthy.",
        "symptoms": ["No disease symptoms detected"],
        "treatment": ["No treatment needed"],
        "prevention": ["Regular monitoring", "Proper pruning and air circulation"]
    },
    # ── Pepper ─────────────────────────────────────────────────────────────────
    "Pepper,_bell___Bacterial_spot": {
        "display_name": "Pepper Bacterial Spot",
        "crop": "Bell Pepper",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "Caused by Xanthomonas campestris pv. vesicatoria, it's a common bacterial disease of peppers.",
        "symptoms": ["Small, water-soaked spots on leaves", "Spots become brown with yellow halos", "Raised, brown scab-like lesions on fruit", "Premature defoliation"],
        "treatment": ["Apply copper bactericide plus mancozeb", "Remove infected plant debris", "Avoid working in fields when plants are wet"],
        "prevention": ["Use disease-free transplants", "Rotate crops every 2-3 years", "Avoid overhead irrigation"]
    },
    "Pepper,_bell___healthy": {
        "display_name": "Healthy Bell Pepper",
        "crop": "Bell Pepper",
        "severity": "None",
        "severity_color": "#27ae60",
        "description": "The pepper plant appears healthy.",
        "symptoms": ["No disease symptoms detected"],
        "treatment": ["No treatment needed"],
        "prevention": ["Crop rotation", "Regular scouting for early detection"]
    },
    # ── Potato ─────────────────────────────────────────────────────────────────
    "Potato___Early_blight": {
        "display_name": "Potato Early Blight",
        "crop": "Potato",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "Caused by Alternaria solani, it produces characteristic target-board lesions on lower leaves.",
        "symptoms": ["Dark brown lesions with concentric rings (target-board pattern)", "Yellow halo surrounding lesions", "Starts on older, lower leaves", "Lesions on stems and tubers in severe cases"],
        "treatment": ["Apply fungicide (chlorothalonil, mancozeb) at first sign", "Remove lower, infected leaves", "Maintain adequate soil fertility"],
        "prevention": ["Use certified disease-free seed potatoes", "Crop rotation", "Adequate fertilization to reduce plant stress"]
    },
    "Potato___Late_blight": {
        "display_name": "Potato Late Blight",
        "crop": "Potato",
        "severity": "Critical",
        "severity_color": "#8e44ad",
        "description": "Caused by Phytophthora infestans — the pathogen responsible for the Irish Potato Famine. Extremely destructive.",
        "symptoms": ["Water-soaked, pale green lesions on leaves that quickly turn brown", "White fuzzy mold on leaf undersides in humid conditions", "Dark, greasy spots on tubers", "Rapid plant collapse in favorable conditions"],
        "treatment": ["Apply fungicide (cymoxanil, metalaxyl) immediately upon detection", "Spray entire field preventatively in high-risk conditions", "Remove and destroy infected plants"],
        "prevention": ["Use resistant varieties", "Apply preventive fungicide during cool, wet weather", "Avoid overhead irrigation"]
    },
    "Potato___healthy": {
        "display_name": "Healthy Potato",
        "crop": "Potato",
        "severity": "None",
        "severity_color": "#27ae60",
        "description": "The potato plant appears healthy.",
        "symptoms": ["No disease symptoms detected"],
        "treatment": ["No treatment needed"],
        "prevention": ["Use certified seed potatoes", "Regular hilling and monitoring"]
    },
    # ── Raspberry ──────────────────────────────────────────────────────────────
    "Raspberry___healthy": {
        "display_name": "Healthy Raspberry",
        "crop": "Raspberry",
        "severity": "None",
        "severity_color": "#27ae60",
        "description": "The raspberry plant appears healthy.",
        "symptoms": ["No disease symptoms detected"],
        "treatment": ["No treatment needed"],
        "prevention": ["Regular pruning of old canes", "Good air circulation"]
    },
    # ── Soybean ────────────────────────────────────────────────────────────────
    "Soybean___healthy": {
        "display_name": "Healthy Soybean",
        "crop": "Soybean",
        "severity": "None",
        "severity_color": "#27ae60",
        "description": "The soybean plant appears healthy.",
        "symptoms": ["No disease symptoms detected"],
        "treatment": ["No treatment needed"],
        "prevention": ["Crop rotation", "Use disease-free seed"]
    },
    # ── Squash ─────────────────────────────────────────────────────────────────
    "Squash___Powdery_mildew": {
        "display_name": "Squash Powdery Mildew",
        "crop": "Squash",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "A very common fungal disease of cucurbits caused by Erysiphe cichoracearum.",
        "symptoms": ["White powdery growth on leaf surfaces", "Yellowing and browning of leaves", "Reduced fruit size and quality", "Can affect stems and fruit"],
        "treatment": ["Apply potassium bicarbonate, neem oil, or sulfur fungicide", "Remove heavily infected leaves", "Improve air circulation"],
        "prevention": ["Plant resistant varieties", "Space plants adequately", "Avoid overhead irrigation"]
    },
    # ── Strawberry ─────────────────────────────────────────────────────────────
    "Strawberry___Leaf_scorch": {
        "display_name": "Strawberry Leaf Scorch",
        "crop": "Strawberry",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "Caused by Diplocarpon earlianum, it weakens plants through repeated defoliation.",
        "symptoms": ["Irregular dark purple spots on leaves", "Spots coalesce causing reddish leaf scorch", "Leaves may dry and fall prematurely", "Reduced runner and fruit production"],
        "treatment": ["Apply captan or myclobutanil fungicide", "Remove infected leaves and plant material", "Renovate beds after harvest"],
        "prevention": ["Plant in well-draining soil", "Avoid overhead irrigation", "Use certified disease-free plants"]
    },
    "Strawberry___healthy": {
        "display_name": "Healthy Strawberry",
        "crop": "Strawberry",
        "severity": "None",
        "severity_color": "#27ae60",
        "description": "The strawberry plant appears healthy.",
        "symptoms": ["No disease symptoms detected"],
        "treatment": ["No treatment needed"],
        "prevention": ["Regular monitoring", "Proper spacing for air movement"]
    },
    # ── Tomato ─────────────────────────────────────────────────────────────────
    "Tomato___Bacterial_spot": {
        "display_name": "Tomato Bacterial Spot",
        "crop": "Tomato",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "Caused by Xanthomonas species, it is one of the most damaging bacterial diseases of tomato.",
        "symptoms": ["Water-soaked leaf spots turning brown with yellow halos", "Raised, brown spots on green fruit", "Severe defoliation in wet conditions", "Stem lesions"],
        "treatment": ["Apply copper bactericide plus mancozeb at first sign", "Avoid handling plants when wet", "Remove and destroy heavily infected plants"],
        "prevention": ["Use disease-free transplants", "Drip irrigation instead of overhead", "Crop rotation of 2-3 years"]
    },
    "Tomato___Early_blight": {
        "display_name": "Tomato Early Blight",
        "crop": "Tomato",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "Caused by Alternaria solani, a very common fungal disease starting on lower leaves.",
        "symptoms": ["Dark brown concentric ring lesions on lower leaves", "Yellow chlorotic halo around lesions", "Stem collar rot in seedlings (damping off)", "Sunken, dark spots with concentric rings on fruit"],
        "treatment": ["Apply fungicide (chlorothalonil, mancozeb, or azoxystrobin)", "Remove lower diseased leaves", "Mulch around plants to prevent soil splash"],
        "prevention": ["Stake and cage plants for air flow", "Crop rotation", "Resistant varieties where available"]
    },
    "Tomato___Late_blight": {
        "display_name": "Tomato Late Blight",
        "crop": "Tomato",
        "severity": "Critical",
        "severity_color": "#8e44ad",
        "description": "Caused by Phytophthora infestans. Can destroy a crop within days under favorable conditions.",
        "symptoms": ["Large, water-soaked, brown lesions on leaves", "White mold on leaf undersides in humid weather", "Brown, firm lesions on green fruit", "Rapid plant collapse"],
        "treatment": ["Apply fungicide (Revus, Forum, Ranman) IMMEDIATELY", "Destroy infected plants — do not compost", "Monitor neighbors' fields"],
        "prevention": ["Plant resistant varieties", "Never overhead irrigate", "Preventive fungicide program in cool, wet periods"]
    },
    "Tomato___Leaf_Mold": {
        "display_name": "Tomato Leaf Mold",
        "crop": "Tomato",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "Caused by Fulvia fulva (syn. Cladosporium fulvum), primarily a greenhouse problem.",
        "symptoms": ["Pale green to yellow spots on upper leaf surface", "Olive-green to brown fuzzy mold on leaf undersides", "Leaves curl, wither, and drop", "Reduced fruit set in severe cases"],
        "treatment": ["Reduce humidity below 85%", "Apply fungicide (chlorothalonil, mancozeb)", "Remove lower infected leaves for air circulation"],
        "prevention": ["Maintain greenhouse humidity below 85%", "Ensure adequate ventilation", "Use resistant greenhouse varieties"]
    },
    "Tomato___Septoria_leaf_spot": {
        "display_name": "Tomato Septoria Leaf Spot",
        "crop": "Tomato",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "Caused by Septoria lycopersici, it defoliates the plant from the bottom up.",
        "symptoms": ["Small, circular spots with dark borders and light gray centers", "Tiny dark dots (pycnidia) visible in lesion centers", "Lower leaves affected first", "Severe defoliation weakens plant and exposes fruit to sunscald"],
        "treatment": ["Apply fungicide (chlorothalonil, copper, mancozeb)", "Remove and destroy infected leaves", "Mulch to prevent soil splash"],
        "prevention": ["Crop rotation of 3 years", "Stake plants for air circulation", "Avoid overhead irrigation"]
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "display_name": "Tomato Spider Mite Damage",
        "crop": "Tomato",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "Two-spotted spider mites (Tetranychus urticae) are a pest — not a disease — but cause significant damage.",
        "symptoms": ["Stippling (tiny dots) on upper leaf surface", "Bronze or silvery sheen on leaves", "Fine webbing on undersides of leaves", "Leaves turn yellow, brown, and die"],
        "treatment": ["Apply miticide (abamectin, bifenazate, spiromesifen)", "Use insecticidal soap or neem oil for organic control", "Strong water spray to dislodge mites"],
        "prevention": ["Monitor regularly, especially in hot, dry weather", "Maintain plant moisture — mites prefer dry conditions", "Avoid excessive nitrogen"]
    },
    "Tomato___Target_Spot": {
        "display_name": "Tomato Target Spot",
        "crop": "Tomato",
        "severity": "Moderate",
        "severity_color": "#f39c12",
        "description": "Caused by Corynespora cassiicola, it produces distinctive target-like lesions.",
        "symptoms": ["Brown circular lesions with concentric rings", "Yellow halo on older lesions", "Affects leaves, stems, and fruit", "Defoliation in severe cases"],
        "treatment": ["Apply fungicide (azoxystrobin, chlorothalonil)", "Improve ventilation and reduce humidity", "Remove infected plant material"],
        "prevention": ["Avoid overhead irrigation", "Crop rotation", "Stake and prune for air circulation"]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "display_name": "Tomato Yellow Leaf Curl Virus",
        "crop": "Tomato",
        "severity": "Severe",
        "severity_color": "#e74c3c",
        "description": "A begomovirus transmitted by the silverleaf whitefly (Bemisia tabaci). A major threat in tropical and subtropical regions.",
        "symptoms": ["Upward curling and yellowing of leaves", "Reduced leaf size and flower drop", "Stunted plant growth", "Little to no fruit set on infected plants"],
        "treatment": ["Remove and destroy infected plants immediately to limit spread", "Control whitefly vector with insecticide (imidacloprid, thiamethoxam)", "Use reflective mulches to repel whiteflies"],
        "prevention": ["Use TYLCV-resistant tomato varieties", "Use insect-proof nets in greenhouses", "Control whitefly populations from transplanting"]
    },
    "Tomato___Tomato_mosaic_virus": {
        "display_name": "Tomato Mosaic Virus",
        "crop": "Tomato",
        "severity": "Severe",
        "severity_color": "#e74c3c",
        "description": "Tomato mosaic virus (ToMV) is highly stable and spreads through contact with infected plant material.",
        "symptoms": ["Light and dark green mosaic pattern on leaves", "Leaf distortion and curling", "Stunted plant growth", "Reduced fruit quality with internal browning"],
        "treatment": ["No chemical cure — remove and destroy infected plants", "Disinfect tools with 10% bleach or 70% alcohol", "Wash hands thoroughly after handling infected plants"],
        "prevention": ["Use virus-free, certified seed", "Plant resistant varieties (Tm-2 gene)", "Disinfect tools and structures regularly", "Control aphid vectors"]
    },
    "Tomato___healthy": {
        "display_name": "Healthy Tomato",
        "crop": "Tomato",
        "severity": "None",
        "severity_color": "#27ae60",
        "description": "The tomato plant appears healthy with no visible disease symptoms.",
        "symptoms": ["No disease symptoms detected"],
        "treatment": ["No treatment needed"],
        "prevention": ["Continue regular monitoring", "Maintain consistent watering", "Balanced fertilization (avoid excess nitrogen)"]
    },
    # ── Banana ─────────────────────────────────────────────────────────────────
    "Banana___healthy": {
        "display_name": "Healthy Banana",
        "crop": "Banana",
        "severity": "None",
        "severity_color": "#27ae60",
        "description": "The banana plant appears healthy with no visible signs of disease.",
        "symptoms": ["No symptoms detected"],
        "treatment": ["No treatment needed"],
        "prevention": ["Regular monitoring", "Maintaining soil moisture"]
    },
    "Banana___Sigatoka": {
        "display_name": "Banana Sigatoka Leaf Spot",
        "crop": "Banana",
        "severity": "Severe",
        "severity_color": "#e74c3c",
        "description": "A devastating fungal disease caused by Mycosphaerella fijiensis.",
        "symptoms": ["Necrotic spots on leaves", "Premature leaf death", "Reduced fruit quality"],
        "treatment": ["Apply mineral oil or systemic fungicides", "Remove infected leaves"],
        "prevention": ["Improve drainage", "Pruning for air circulation"]
    },
}

# Fallback for unknown classes
DEFAULT_INFO = {
    "display_name": "Unknown Condition",
    "crop": "Unknown",
    "severity": "Unknown",
    "severity_color": "#95a5a6",
    "description": "This condition or crop is not yet in our detailed diagnostic database. Please consult an expert.",
    "symptoms": ["Unable to provide specific symptoms"],
    "treatment": ["Consult a local agricultural extension officer"],
    "prevention": ["Continue regular scouting and monitoring"]
}

UNCERTAIN_INFO = {
    "display_name": "Inconclusive Analysis",
    "crop": "Indeterminate",
    "severity": "N/A",
    "severity_color": "#bdc3c7",
    "description": "The AI is currently uncertain about this image. This may be due to poor lighting, non-leaf content, or an unsupported crop.",
    "symptoms": ["No clear symptoms identified"],
    "treatment": ["Try taking a clearer, closer photo of the infected leaf area."],
    "prevention": ["Ensure the crop is among the 14 supported species."]
}


def get_disease_info(class_name: str) -> dict:
    """Return disease info for a given class name, with fallback and pro features."""
    if class_name == "UNCERTAIN":
        info = {**UNCERTAIN_INFO}
    else:
        info = DISEASE_INFO.get(class_name, {**DEFAULT_INFO, "display_name": class_name.replace("__", " - ").replace("_", " ")})
    
    # --- Inject AgriScan Pro Metadata ---
    severity = info.get("severity", "Moderate")
    crop = info.get("crop", "Unknown")
    
    # 1. Economic Impact Factor (0.0 to 1.0)
    impact_map = {"None": 0.0, "Low": 0.15, "Moderate": 0.35, "Severe": 0.65, "Critical": 0.85, "N/A": 0.0, "Unknown": 0.2}
    info["impact_factor"] = impact_map.get(severity, 0.4)
    
    # 2. Market Price (Baseline INR per acre)
    price_map = {
        "Apple": 150000, "Tomato": 85000, "Potato": 70000, "Grape": 250000,
        "Corn (Maize)": 45000, "Orange": 120000, "Peach": 180000, "Bell Pepper": 95000,
        "Strawberry": 300000, "Cherry": 220000, "Soybean": 40000, "Blueberry": 350000,
        "Banana": 110000, "Squash": 60000, "Raspberry": 280000
    }
    info["market_price_acre"] = price_map.get(crop, 50000)
    
    # 3. Weather Progression Triggers
    weather_map = {
        "Moderate": "Progression likely in humid conditions (RH > 80%).",
        "Severe": "Rapid spread expected in cool, wet weather.",
        "Critical": "Extreme risk: Spread can double daily in rain.",
        "None": "Environment is stable for current crop health.",
        "N/A": "Environmental triggers not applicable."
    }
    info["weather_risk"] = weather_map.get(severity, "Standard monitoring recommended.")
    
    # 4. Recovery Nutrient Advice
    nutrient_map = {
        "Tomato": ["Apply Calcium-Boron for cell strength.", "Reduce Nitrogen to avoid soft tissue."],
        "Potato": ["High Potassium (K) helps build resistance.", "Avoid soil waterlogging."],
        "Apple": ["Zinc/Manganese for healthy bark.", "Ensure pH (6.0-6.5)."],
        "Banana": ["Maintain high Potassium (K) levels.", "Improve drainage to prevent root rot."]
    }
    info["nutrient_tips"] = nutrient_map.get(crop, ["Maintain balanced N-P-K (19:19:19).", "Ensure adequate irrigation drainage."])
    
    return info
