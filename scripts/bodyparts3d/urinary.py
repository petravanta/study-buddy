# Picture jobs for the urinary chapter, read by jobs.py: the kidneys, ureters, bladder and urethra drawn see-through inside
# the lower trunk, with one part in red. BodyParts3D has no nephron or kidney interior, so those are text questions.
URO = ids(r'kidney$', r'ureter$', r'^urinary bladder$', r'^urethra$', r'adrenal gland')
URO_V = ids(r'renal (artery|vein)', r'^inferior vena cava$', r'(descending|ascending) aorta', r'common iliac (artery|vein)')
URO_BONES = ids(r'\brib$', r'costal cartilage', r'thoracic vertebra', r'lumbar vertebra', r'^sacrum$', r'hip bone', r'right femur$', r'left femur$')
def ur(name, *pats, view='front', focus=None, xray=True, extra=(), pad=1.15, w=800, h=800, **kw):
    hi = ids(*pats)
    J[name] = {'view': view, 'hi': hi, 'focus': focus or ids(r'kidney$', r'^urinary bladder$'), 'only': URO_BONES + URO + URO_V + ids(*extra), 'xray': xray, 'w': w, 'h': h, 'pad': pad, **kw}
ur('u-system', r'kidney$', r'ureter$', r'^urinary bladder$', r'^urethra$', focus=ids(r'kidney$', r'^urinary bladder$', r'^urethra$'))
ur('u-kidneys', r'kidney$')
ur('u-right-kidney', r'right kidney')
ur('u-left-kidney', r'left kidney')
ur('u-ureters', r'ureter$')
ur('u-bladder', r'^urinary bladder$', focus=ids(r'^urinary bladder$', r'ureter$', r'^urethra$', r'hip bone'), pad=1.5)
ur('u-adrenals', r'adrenal gland', focus=ids(r'kidney$', r'adrenal gland'), pad=1.4)
ur('u-renal-arteries', r'renal artery', focus=ids(r'kidney$'), pad=1.4)
ur('u-renal-veins', r'renal vein', focus=ids(r'kidney$'), pad=1.4)
