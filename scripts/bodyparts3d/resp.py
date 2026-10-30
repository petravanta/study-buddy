# Picture jobs for the respiratory chapter, read by jobs.py: the lungs and airways drawn see-through inside the rib cage,
# with one part in red. BodyParts3D has the lung lobes, the trachea and the main bronchi, plus the diaphragm (a muscle).
RIBCAGE = ids(r'\brib$', r'costal cartilage', r'^manubrium$', r'^body of sternum$', r'^xiphoid', r'clavicle', r'thoracic vertebra', r'^atlas$', r'^axis$', r'cervical vertebra', r'thyroid cartilage', r'^hyoid')
RFOCUS = LUNGS + AIRWAYS
def rs(name, *pats, view='front', focus=None, xray=True, bones=True, pad=1.12, w=800, h=800, **kw):
    hi = ids(*pats)
    only = (RIBCAGE if bones else []) + LUNGS + AIRWAYS + ids(r'^diaphragm$')
    J[name] = {'view': view, 'hi': hi, 'focus': focus or RFOCUS, 'only': only, 'xray': xray, 'w': w, 'h': h, 'pad': pad, **kw}
rs('r-lungs', r'lobe of', xray=True)
rs('r-airways', r'trachea', r'bronchus')
rs('r-trachea', r'trachea')
rs('r-bronchi', r'bronchus', pad=1.5, focus=AIRWAYS + LUNGS)
rs('r-upper-lobe-right', r'upper lobe of right lung')
rs('r-middle-lobe', r'middle lobe of lung')
rs('r-lower-lobe-right', r'lower lobe of right lung', view='back')
rs('r-upper-lobe-left', r'upper lobe of left lung')
rs('r-lower-lobe-left', r'lower lobe of left lung', view='back')
rs('r-right-lung', r'right lung', r'(upper|lower) lobe of right lung', r'middle lobe')
rs('r-left-lung', r'(upper|lower) lobe of left lung')
rs('r-diaphragm', r'^diaphragm$', view=[0, -1, .3])
