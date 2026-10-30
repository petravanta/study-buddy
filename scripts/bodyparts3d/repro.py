# Picture jobs for the reproductive chapter, read by jobs.py: the male reproductive organs drawn see-through inside the
# pelvis, with one part in red. BodyParts3D has no female reproductive organs, so those are text questions.
REP = ids(r'testis$', r'epididymis$', r'deferent duct$', r'seminal vesicle$', r'^prostate$', r'^urethra$', r'^urinary bladder$',
          r'glans penis', r'corpus (cavernosum|spongiosum) of penis')
REP_BONES = ids(r'hip bone', r'^sacrum$', r'lumbar vertebra', r'right femur$', r'left femur$')
def rp(name, *pats, view='front', focus=None, xray=True, extra=(), pad=1.2, w=800, h=800, **kw):
    hi = ids(*pats)
    J[name] = {'view': view, 'hi': hi, 'focus': focus or REP, 'only': REP_BONES + REP + ids(*extra), 'xray': xray, 'w': w, 'h': h, 'pad': pad, **kw}
rp('x-system', r'testis$', r'epididymis$', r'deferent duct$', r'seminal vesicle$', r'^prostate$', r'glans penis', r'corpus (cavernosum|spongiosum) of penis', pad=1.1)
rp('x-testes', r'testis$', focus=ids(r'testis$', r'epididymis$'), pad=1.5)
rp('x-epididymides', r'epididymis$', focus=ids(r'testis$', r'epididymis$'), pad=1.5)
rp('x-deferent-ducts', r'deferent duct$', pad=1.2)
rp('x-seminal-vesicles', r'seminal vesicle$', focus=ids(r'seminal vesicle$', r'^prostate$', r'^urinary bladder$'), pad=1.5, view='back')
rp('x-prostate', r'^prostate$', focus=ids(r'^prostate$', r'seminal vesicle$', r'^urinary bladder$'), pad=1.5, view='left')
rp('x-penis', r'corpus (cavernosum|spongiosum) of penis', r'glans penis', focus=ids(r'glans penis', r'corpus (cavernosum|spongiosum) of penis'), pad=1.3, view='left')
rp('x-glans', r'glans penis', focus=ids(r'glans penis', r'corpus (cavernosum|spongiosum) of penis'), pad=1.3, view='left')
rp('x-corpus-cavernosum', r'corpus cavernosum of penis', focus=ids(r'glans penis', r'corpus (cavernosum|spongiosum) of penis'), pad=1.3, view='left')
rp('x-corpus-spongiosum', r'corpus spongiosum of penis', focus=ids(r'glans penis', r'corpus (cavernosum|spongiosum) of penis'), pad=1.3, view='left')
