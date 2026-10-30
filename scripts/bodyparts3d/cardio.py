# Picture jobs for the cardiovascular chapter, read by jobs.py: the heart and the large vessels, drawn see-through over the
# skeleton, with one part in red. BodyParts3D has the heart as one wall (no chambers), its valves and papillary muscles,
# the coronary arteries and cardiac veins, and the large arteries and veins of the trunk and neck.
CHEST = ids(r'wall of heart', r'ascending aorta', r'arch of aorta', r'superior vena cava', r'pulmonary (artery|vein)', r'brachiocephalic', r'common carotid', r'subclavian (artery|vein)')
TRUNK_V = ARTERIES + VEINS
def cv(name, *pats, view='front', focus=None, ctx='all', xray=True, hide=(), pad=1.15, w=800, h=800, **kw):
    hi = ids(*pats)
    only = {'all': ALL + HEART + ARTERIES + VEINS, 'heart': HEART, 'vessels': HEART + ARTERIES + VEINS, 'chest': ids(r'rib$', r'costal cartilage', r'sternum|manubrium|xiphoid', r'clavicle', r'thoracic vertebra') + HEART + ARTERIES + VEINS}[ctx]
    J[name] = {'view': view, 'hi': hi, 'focus': focus or hi, 'only': [i for i in only if i not in set(hide)], 'xray': xray, 'w': w, 'h': h, 'pad': pad, **kw}
HEART_FOCUS = ids(r'wall of heart')
VESSEL_FOCUS = ids(r'wall of heart', r'common iliac artery', r'common carotid')
# The heart
cv('c-heart', r'wall of heart', focus=HEART_FOCUS, ctx='chest', pad=1.7)
cv('c-tricuspid', r'tricuspid valve', focus=HEART_FOCUS, ctx='heart', pad=1.3)
cv('c-mitral', r'mitral valve', focus=HEART_FOCUS, ctx='heart', pad=1.3)
cv('c-pulmonary-valve', r'pulmonary valve', focus=HEART_FOCUS, ctx='heart', pad=1.3)
cv('c-papillary', r'papillary muscle', focus=HEART_FOCUS, ctx='heart', pad=1.3)
cv('c-coronary-arteries', r'coronary artery', focus=HEART_FOCUS, ctx='vessels', pad=1.3, xray=False, hide=ids(r'wall of heart') and [])
cv('c-right-coronary', r'(trunk|marginal branch|posterior interventricular branch|posterolateral branch|set of interventricular septal branches) of right coronary|right coronary artery', focus=HEART_FOCUS, ctx='vessels', pad=1.3)
cv('c-left-coronary', r'stem of left coronary', r'anterior interventricular branch', focus=HEART_FOCUS, ctx='vessels', pad=1.3)
cv('c-circumflex', r'circumflex branch', focus=HEART_FOCUS, ctx='vessels', pad=1.3)
cv('c-great-cardiac-vein', r'great cardiac vein', focus=HEART_FOCUS, ctx='vessels', pad=1.3)
cv('c-coronary-sinus', r'coronary sinus', focus=HEART_FOCUS, ctx='vessels', pad=1.3, view='back')
# Large arteries
AORTA = ids(r'ascending aorta', r'arch of aorta', r'descending aorta')
cv('c-aorta', r'ascending aorta', r'arch of aorta', r'descending aorta', focus=VESSEL_FOCUS + AORTA, w=600, h=1000)
cv('c-ascending-aorta', r'ascending aorta', focus=HEART_FOCUS, ctx='chest', pad=1.4)
cv('c-aortic-arch', r'arch of aorta', focus=CHEST, ctx='chest')
cv('c-descending-aorta', r'descending aorta', focus=VESSEL_FOCUS + AORTA, w=600, h=1000)
cv('c-brachiocephalic-artery', r'brachiocephalic artery', focus=CHEST, ctx='chest')
cv('c-common-carotid', r'common carotid', focus=CHEST, ctx='chest')
cv('c-subclavian-artery', r'subclavian artery', focus=CHEST, ctx='chest')
cv('c-pulmonary-artery', r'pulmonary artery', focus=HEART_FOCUS, ctx='chest', pad=1.4)
cv('c-celiac', r'celiac artery', r'common hepatic', r'left gastric', r'splenic artery', focus=ids(r'celiac artery', r'splenic artery'), ctx='all', pad=2.2)
cv('c-celiac-trunk', r'celiac artery', focus=ids(r'celiac artery', r'superior mesenteric artery'), ctx='all', pad=3)
cv('c-sup-mesenteric', r'superior mesenteric artery', focus=ids(r'celiac artery', r'inferior mesenteric artery'), ctx='all', pad=2)
cv('c-inf-mesenteric', r'inferior mesenteric artery', focus=ids(r'celiac artery', r'common iliac artery'), ctx='all', pad=1.5)
cv('c-renal-artery', r'renal artery', focus=ids(r'renal (artery|vein)'), ctx='all', pad=2.5)
cv('c-common-iliac-artery', r'common iliac artery', focus=ids(r'common iliac', r'internal iliac', r'external iliac'), ctx='all', pad=1.5)
cv('c-external-iliac-artery', r'external iliac artery', focus=ids(r'common iliac', r'internal iliac', r'external iliac'), ctx='all', pad=1.5)
cv('c-internal-iliac-artery', r'internal iliac artery', focus=ids(r'common iliac', r'internal iliac', r'external iliac'), ctx='all', pad=1.5)
# Large veins
cv('c-svc', r'superior vena cava', focus=CHEST, ctx='chest')
cv('c-ivc', r'inferior vena cava', focus=ids(r'inferior vena cava', r'common iliac vein'), ctx='all', w=600, h=1000, pad=1.4)
cv('c-brachiocephalic-vein', r'brachiocephalic vein', focus=CHEST, ctx='chest')
cv('c-jugular', r'internal jugular', focus=CHEST, ctx='chest')
cv('c-subclavian-vein', r'subclavian vein', focus=CHEST, ctx='chest')
cv('c-pulmonary-vein', r'pulmonary vein', focus=HEART_FOCUS, ctx='chest', pad=1.4, view='back')
cv('c-renal-vein', r'renal vein', focus=ids(r'renal (artery|vein)'), ctx='all', pad=2.5)
cv('c-common-iliac-vein', r'common iliac vein', focus=ids(r'common iliac', r'internal iliac', r'external iliac'), ctx='all', pad=1.5)
cv('c-splenic-vein', r'splenic vein', r'superior mesenteric vein', focus=ids(r'splenic vein', r'superior mesenteric'), ctx='all', pad=2)
