# Picture jobs for the endocrine chapter, read by jobs.py. The pituitary, pineal and hypothalamus pictures come from the
# nervous chapter (b-*), the adrenals from the urinary one (u-adrenals), the pancreas from the digestive one (d-pancreas)
# and the testes from the reproductive one (x-testes). BodyParts3D has no thyroid, parathyroid or ovary models.
ENDO = ids(r'lobe of thymus', r'adrenal gland', r'^pancreas', r'testis$')
ENDO_CTX = ids(r'^wall of heart$', r'lobe of (right|left) lung', r'kidney$', r'^liver$', r'^stomach$', r'^duodenum$', r'^spleen$')
def en(name, *pats, view='front', focus=None, xray=True, extra=(), pad=1.15, w=800, h=800, **kw):
    hi = ids(*pats)
    J[name] = {'view': view, 'hi': hi, 'focus': focus or ENDO, 'only': TRUNK_BONES + ENDO + ENDO_CTX + ids(*extra), 'xray': xray, 'w': w, 'h': h, 'pad': pad, **kw}
en('e-system', r'lobe of thymus', r'adrenal gland', r'^pancreas', r'testis$', pad=1.05)
en('e-thymus', r'lobe of thymus', focus=ids(r'lobe of thymus', r'^wall of heart$'), pad=1.6)
