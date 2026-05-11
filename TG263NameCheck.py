import re
import difflib
import argparse
from datetime import datetime
import pandas as pd


def validate_tg263(input_string: str):

    tg263roots = [
        "A_Aorta", "A_Aorta_Asc", "A_Brachiocephls", "A_Carotid", "A_Celiac",
        "A_Coronary", "A_Femoral", "A_Femoral_Cflx", "A_Humeral", "A_Humeral_Cflx",
        "A_Hypophyseal", "A_Iliac", "A_Iliac_Cflx", "A_Iliac_Ext", "A_Iliac_Int",
        "A_LAD", "A_Mesenteric", "A_Pulmonary", "A_Subclavian", "A_Vertebral",
        "Acetabulum", "Acetabulums", "AirWay", "Anus", "Appendix",
        "Arytenoid", "Atrium", "Bag_Bowel", "Bag_Ostomy", "BileDuct_Common",
        "Bladder", "Body", "BODY","Bolus", "Bone", "Bone_Ethmoid",
        "Bone_Frontal", "Bone_Hyoid", "Bone_Ilium", "Bone_Incus", "Bone_Ischium",
        "Bone_Lacrimal", "Bone_Mandible", "Bone_Mastoid", "Bone_Nasal", "Bone_Occipital",
        "Bone_Palatine", "Bone_Parietal", "Bone_Pelvic", "Bone_Sphenoid", "Bone_Temporal",
        "Bone_Zygomatic", "Bone_Zygomatics", "BoneMarrow", "BoneMarrow_Act", "Boost",
        "Bowel", "Bowel_Bag", "Bowel_Large", "Bowel_Small", "BrachialPlex",
        "BrachialPlexs", "Brain", "Brainstem", "Brainstem_Core", "Brainstem_Surf",
        "Breast", "Breasts", "Bronchus", "Bronchus_Main", "Canal_Anal",
        "Carina", "Cartlg_Thyroid", "CaudaEquina", "Cavernosum", "Cavity_Nasal",
        "Cavity_Oral", "Cecum", "Cerebellum", "Cerebrum", "Cervix",
        "Chestwall", "Cist_Pontine", "Cist_Suprasellar", "Clavicle", "CN_III",
        "CN_IX", "CN_V", "CN_VI", "CN_VII", "CN_VIII",
        "CN_XI", "CN_XII", "Cochlea", "Colon", "Colon_Ascending",
        "Colon_Decending", "Colon_Sigmoid", "Colon_Transverse", "Cornea", "Cornea_L",
        "Cornea_R", "CribriformPlate", "Cricoid", "Cricopharyngeus", "CTV",
        "Dens", "Diaphragm", "Duodenum", "Ear_External", "Ear_Externals",
        "Ear_Internal", "Ear_Internals", "Ear_Middle", "Edema", "Elbow",
        "Elbow_L", "Esophagus", "Eval", "External", "Eye",
        "Eyes", "Femur", "Femur_Base", "Femur_Head", "Femur_Joint",
        "Femur_Neck", "Femur_Shaft", "Femur_Shafts", "Femurs", "Fibula",
        "Foley", "Fossa_Jugular", "Fossa_Posterior", "Gallbladder", "Genitals",
        "Glnd_Adrenal", "Glnd_Adrenals", "Glnd_Lacrimal", "Glnd_Lacrimals", "Glnd_Parathyroid",
        "Glnd_Subling", "Glnd_Sublings", "Glnd_Submand", "Glnd_Submands", "Glnd_Thymus",
        "Glnd_Thyroid", "Glottis", "GreatVes", "GrowthPlate", "GTV",
        "Hardpalate", "Heart", "Hemisphere", "Hemispheres", "Hippocampi",
        "Hippocampus", "Humerus", "Hypothalmus", "ICTV", "IDL",
        "IGTV", "Ileum", "ITV", "Jejunum", "Jejunum_Ileum",
        "Joint_Elbow", "Joint_Elbow_L", "Joint_Elbow_R", "Joint_Glenohum", "Joint_Surface",
        "Joint_TM", "Kidney", "Kidney_Cortex", "Kidney_Hilum", "Kidney_Hilums",
        "Kidney_Pelvis", "Kidneys", "Knee", "Laryngl_Pharynx", "Larynx",
        "Larynx_SG", "Leads", "Lens", "Lig_Hepatogastrc", "Lips",
        "Liver", "Liver-CTV", "Liver-GTV", "LN", "LN_Ax",
        "LN_Ax_Apical", "LN_Ax_Central", "LN_Ax_Centrals", "LN_Ax_L1", "LN_Ax_L2",
        "LN_Ax_L3", "LN_Ax_Lateral", "LN_Ax_Laterals", "LN_Ax_Pectoral", "LN_Ax_Pectorals",
        "LN_Ax_Subscap", "LN_Ax_Subscaps", "LN_Brachioceph", "LN_Brachiocephs", "LN_Bronchpulm",
        "LN_Bronchpulms", "LN_Diaphragmatic", "LN_Iliac", "LN_Iliac_Ext", "LN_Iliac_Int",
        "LN_IMN", "LN_IMNs", "LN_Inguinofem", "LN_Intercostal", "LN_Intercostals",
        "LN_Ligamentarter", "LN_lliac_Int", "LN_Mediastinals", "LN_Neck_IA", "LN_Neck_IB",
        "LN_Neck_II", "LN_Neck_IIA", "LN_Neck_IIB", "LN_Neck_III", "LN_Neck_IV",
        "LN_Neck_V", "LN_Neck_VA", "LN_Neck_VB", "LN_Neck_VC", "LN_Neck_VI",
        "LN_Neck_VII", "LN_Obturator", "LN_Paraaortic", "LN_Paramammary", "LN_Paramammarys",
        "LN_Parasternal", "LN_Parasternals", "LN_Pelvic", "LN_Pelvics", "LN_Portahepatis",
        "LN_Presacral", "LN_Pulmonary", "LN_Pulmonarys", "LN_Sclav", "LN_Supmammary",
        "LN_Trachbrnchs", "Lobe_Frontal", "Lobe_Occipital", "Lobe_Parietal", "Lobe_Temporal",
        "Lung", "Lung_LLL", "Lung_LUL", "Lung_RLL", "Lung_RML",
        "Lung_RUL", "Lungs", "Lungs-CTV", "Lungs-GTV", "Lungs-ITV",
        "Lungs-PTV", "Malleus", "Markers", "Maxilla", "Mediastinum",
        "Musc", "Musc_Constrict", "Musc_Digastric", "Musc_Masseter", "Musc_Platysma",
        "Musc_Pterygoid", "Musc_Sclmast", "Musc_Temporal", "Nasalconcha", "Nasopharynx",
        "Nose", "Nrv_Peripheral", "Nrv_Root", "OpticChiasm", "OpticNrv",
        "Orbit", "Oropharynx", "Ovaries", "Ovary", "Pacemaker",
        "Palate_Soft", "PancJejuno", "Pancreas", "Pancreas_Head", "Pancreas_Tail",
        "Parametrium", "Parotid_L", "Parotid_R", "Parotids", "Pelvis","PenileBulb",
        "Penis", "Pericardium", "Perineum", "Peritoneum", "Pharynx",
        "Pineal", "Pituitary", "Pons", "Postop", "Preop",
        "Proc_Condyloid", "Proc_Coronoid", "Prostate", "ProstateBed", "Prosthesis",
        "Pterygoid_Lat", "Pterygoid_Med", "PTV", "PTV!", "PubicSymphys",
        "Radius", "Rectal", "Rectum", "Retina", "Retinas",
        "Rib", "Rib01", "Rib02", "Rib03", "Rib04",
        "Rib05", "Rib06", "Rib07", "Rib08", "Rib09",
        "Rib10", "Rib11", "Rib12", "Rib13", "SacralPlex",
        "Sacrum", "Scalp", "Scapula_L", "Scapula_R", "Scar",
        "Scar_Boost", "Scrotum", "SeminalVes", "Sinus_Ethmoid", "Sinus_Frontal",
        "Sinus_Maxilry", "Sinus_Sphenoid", "Skin", "Skin_Perineum", "Skin_Peritoneum",
        "Skull", "Spc", "Spc_Bowel ", "Spc_Bowel_Small", "Spc_Retrophar",
        "Spc_Retrophars", "Spc_Retrosty", "Spc_Supraclav", "Sphincter_Anal", "SpinalCanal",
        "SpinalCord", "SpinalCord_Cerv", "SpinalCord_Lum", "SpinalCord_Sac", "SpinalCord_Thor",
        "Spleen", "Spleen_Hilum", "Spongiosum", "Stapes", "Stomach",
        "Strct ", "Strct_Suprapatel", "Surf_Eye", "SurgicalBed", "Sys_Ventricular",
        "Tendon ", "Tendon_Quad", "Testis", "ThecalSac", "Thoracic_Duct",
        "Tongue", "Tongue_All", "Tongue_Base", "Tongue_Oral", "Tonsil",
        "Trachea", "TumorBed", "Ureter_L", "Ureter_R", "UreterDivert",
        "Ureters", "Urethra", "Urethra_Prostatc", "Uterus", "V_Azygos",
        "V_Brachioceph", "V_Iliac", "V_Iliac_Ext", "V_Iliac_Int", "V_Jugular",
        "V_Jugular_Ext", "V_Jugular_Int", "V_Portal", "V_Pulmonary", "V_Subclavian",
        "V_Subclavians", "V_Venacava", "Vagina", "Vagina_Surf", "VaginalCuff",
        "Valve", "Valve_Aortic", "Valve_Mitral", "Valve_Pulmonic", "Valve_Tricuspid",
        "VB", "VB_C", "VB_C1", "VB_C2", "VB_C3",
        "VB_C4", "VB_C5", "VB_C6", "VB_C7", "VB_L",
        "VB_L1", "VB_L2", "VB_L3", "VB_L4", "VB_L5",
        "VB_S", "VB_S1", "VB_S2", "VB_S3", "VB_S4",
        "VB_S5", "VB_T", "VB_T01", "VB_T02", "VB_T03",
        "VB_T04", "VB_T05", "VB_T06", "VB_T07", "VB_T08",
        "VB_T09", "VB_T10", "VB_T11", "VB_T12", "VBs",
        "Ventricle", "VocalCord", "VocalCords", "Vomer", "Vulva"]
    
    

    # STEP 1: Split on ^ and take the left side
    name = re.split(r'\^', input_string)[0].strip()

    if not name:
        return "Invalid", name, None, False
    
    is_trainee_structure = False
    if re.match(r'^(?:zTS_?|_TS_?)', name):
        is_trainee_structure = True
        name = re.sub(r'^(?:zTS_?|_TS_?)', '', name)
  
        
    # Categorize Trainee Structures 

    nearest_match = None
    is_exact_match = False
    # STEP 3: Categorize Target vs OAR
    target_prefixes = ("GTV", "CTV", "ITV", "IGTV", "ICTV", "PTV", "PTV!")

    # Categorize structures
    if not name:
        category = "Invalid"      
    elif name.lower().startswith('z') or name.startswith('_'):
        category = "Ignore"
    elif name.upper().startswith(target_prefixes):
        category = "Target"
    else:
        category = "NonTarget"



    if category == "NonTarget" :   
        # Remove qualifiers
        qualifiers = ['_DCMtags', '_DO']
        name = next((name[:-len(q)] for q in qualifiers if name.endswith(q)), name)

        # Remove PRV Designator
        m = re.match(r'^(.+)_PRV(\d{2})?$', name)
        if m:
            name = m.group(1)

        # Remove Wall Designator
        m = re.match(r'^(.+)_Wall(\d{2})?$', name)
        if m:
            name = m.group(1)

        # Remove Spatial Designators
        spatialdesignators_end = [
            '_NAdj', '_Dist', '_Prox',
            '_L', '_R', '_A', '_P', '_I', '_S','_M',
            '_LS', '_LI','_RS', '_RI'
        ]

        spatialdesignators_start = [
            'NAdj_', 'Dist_', 'Prox_',
            'L_', 'R_', 'A_', 'P_', 'I_', 'S_','M_',
            'LS_', 'LI_','RS_', 'RI_'
        ]

        name = next((name[:-len(q)] for q in spatialdesignators_end  if name.endswith(q)),   name)
        name = next((name[len(q):]  for q in spatialdesignators_start if name.startswith(q)), name)

        # Remove partial structure Designator
        partialstructuredesignator = ['~']
        name = next((name[:-len(q)] for q in partialstructuredesignator if name.endswith(q)), name)


    elif category == "Target":
        
        # Remove imaging modality qualifier (e.g., _CT, _PT1, _PT1CT1)
        name = re.sub(r'_(?:(?:CT|PT|MR|SP)\d*)+$', '', name)

        # Remove respiratory management qualifiers    
        name = re.sub(r'_(?:(?:FB|BH|EXBH|INBH|Avg|Amp|Min|MinIP)\d*)+$', '', name)

        # Remove Respiratory Phase management qualifiers (e.g., _Phase1, _Phase12, _Phase1-2, _Phase12-34)
        name = re.sub(r'_Phase\d+(?:-\d+)?$', '', name)
        
        # Remove Revision Qualifier (e.g., _Rev1, _Rev2)
        name = re.sub(r'_Rev\d+$', '', name)

        # Remove Retreatment Qualifier (e.g.,_ReTx1, _ReTx2)
        name = re.sub(r'_ReTx\d+$', '', name)

        # Remove Expansion Volume Qualifier (e.g., _Exp1, _Exp2)
        name = re.sub(r'_EV\d+$', '', name)

        # Remove Cropping Qualifier (e.g. -03, -05  etc.)
        name = re.sub(r'-\d{2}$', '', name)

        # Remove dose-fractionation Qualifier(e.g., _4500cGyx25, _45p0Gyx5)
        name = re.sub(r'_(?:\d{4}|\d{2}p?\d)c?Gyx\d+$', '', name)

        # Remove -<tg263root>_PRV<XX> or NOT<tg263root>_PRV<XX> suffix (e.g., -Heart_PRV05, NOTLung_PRV10)
        prv_suffix_pattern = r'(?:-|NOT|AND)(?:' + '|'.join(re.escape(r) for r in tg263roots) + r')(?:_PRV\d+)?$'
        name = re.sub(prv_suffix_pattern, '', name)
        
        # Remove Low/High Dose Designators
        qualifiers = ['_Low', '_High']
        name = next((name[:-len(q)] for q in qualifiers if name.endswith(q)), name)

        # Remove _Mid Designator
        m = re.match(r'^(.+)_Mid(\d{2})?$', name)
        if m:
            name = m.group(1)

        # Remove relative dose Designator with numeric value (e.g., _50Gy, _80cGy)
        nameout = re.sub(r'_\d+(?:c?Gy)?$', '', name)
        if nameout != name:
            category = category + " + Dose"
        name = nameout

        # Remove numerical Designators for numbering targets (e.g., 01, 02, etc.)
        nameout = re.sub(r'\d{2}+$', '', name)
        if nameout != name:
            category = category + " + Enumerated"
        name = nameout

        # Remove target risk level designators(e.g., GTVpHR, GTVnLR)
        name = re.sub(r'(HR|IR|LR)$', '', name)


        # Remove Spatial Designators
        spatialdesignators_end = [
            '_NAdj', '_Dist', '_Prox',
            '_L', '_R', '_A', '_P', '_I', '_S','_M',
            '_LS', '_LI','_RS', '_RI'
        ]

        spatialdesignators_start = [
            'NAdj_', 'Dist_', 'Prox_',
            'L_', 'R_', 'A_', 'P_', 'I_', 'S_','M_',
            'LS_', 'LI_','RS_', 'RI_'
        ]

        name = next((name[:-len(q)] for q in spatialdesignators_end  if name.endswith(q)),   name)
        name = next((name[len(q):]  for q in spatialdesignators_start if name.startswith(q)), name)


        # Remove _<tg263root> suffix (e.g., _Lung, _Heart)
        root_suffix_pattern = r'_(?:' + '|'.join(re.escape(r) for r in tg263roots) + r')$'
        name = re.sub(root_suffix_pattern, '', name)



        # Remove target classifier designators(e.g., GTVn, GTVp)
        name = re.sub(r'(n|p|sb|par|v|vas)$', '', name)

    # Find nearest match in tg263roots
    matches = difflib.get_close_matches(name, tg263roots, n=1, cutoff=0.0)
    nearest_match = matches[0] if matches else None
    is_exact_match = nearest_match is not None and nearest_match == name

    if not is_exact_match and ((category == "Target") or (category == "NonTarget") ):
        category = "Invalid"
    
    if is_trainee_structure:
        category = "Trainee " + category

    return category, name, nearest_match


# --- Test Cases ---



test_data = [
    "Lung_RUL^1",      # OAR (Root: Lung)
    "Kidney_L",        # OAR (Root: Kidney)
    "PTV_Pelvis",      # Target
    "Heart_NAdj^Scan", # OAR (Root: Heart)
    "z_Test",          # Ignore
    "Femur_Head_R",    # OAR (Root: Femur_Head)
    "GTVp",      
    "PTV-Lungs",  
    "PTV_Lung_R", 
    "zTS_Heart",      # Trainee Target
    "Fred"   # Target
]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TG263 Name Checker')
    parser.add_argument('-type', dest='mode', choices=['single', 'file'], required=True,
                        help='single: check one name; file: process an input file')
    parser.add_argument('positional', nargs='*',
                        help='single: <name>   file: <input_file> [output_file]')
    args = parser.parse_args()

    if args.mode == 'single':
        if len(args.positional) != 1:
            parser.error('single mode requires exactly one structure name argument')
        category, filtered, nearest = validate_tg263(args.positional[0])
        print(f"Category:     {category}")
        print(f"FilteredName: {filtered}")
        print(f"NearestTG263: {nearest}")

    else:  # file mode
        if len(args.positional) == 0:
            parser.error('file mode requires an input file argument')
        input_path = args.positional[0]
        output_path = (args.positional[1] if len(args.positional) >= 2
                       else f"output{datetime.now().strftime('%Y%m%d%H%M')}.xlsx")

        inputdf = pd.read_csv(
            input_path,
            sep='\t',
            header=None,
            dtype=str
        )

        results = inputdf[5].apply(validate_tg263)
        outputdf = inputdf[[0, 1, 2, 5]].copy()
        outputdf.columns = ['MRN', 'CourseId', 'PlanId', 'StructureId']
        outputdf['Category']     = results.apply(lambda x: x[0])
        outputdf['FilteredName'] = results.apply(lambda x: x[1])
        outputdf['NearestTG263'] = results.apply(lambda x: x[2])

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            outputdf.to_excel(writer, index=False)
            ws = writer.sheets['Sheet1']
            for cell in ws['A'][1:]:  # skip header row
                cell.number_format = '@'
        print(f"Written {len(outputdf)} rows to {output_path}")
