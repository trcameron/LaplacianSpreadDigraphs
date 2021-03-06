# Restricted Numerical Range Functions
from numpy import argsort, array, conj, cos, diag, dot, exp, eye, imag, pi, real, sin, sum, transpose, zeros
from numpy.linalg import eigh, eigvals, eigvalsh, norm
from networkx import DiGraph, draw_shell
from sys import stdin
from matplotlib import pyplot as plt
from functools import lru_cache

# Tolerance Parameters
EPS = 2**(-52)
TOL = 2**(-42)
TOL2 = 2**(-18)

###############################################
###             Cmplx Convex Hull           ###
###############################################
def cmplxConvHull(points):
    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(points))
    # Boring case: no points or a single point, possibly repeated multiple times.
    if(len(points) <= 1):
        return points
    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def _cross(o, a, b):
        return (a.real - o.real)*(b.imag - o.imag) - (a.imag - o.imag)*(b.real-o.real)
    # Build lower hull
    lower = []
    for p in points:
        while((len(lower)>=2) and (_cross(lower[-2],lower[-1],p)<EPS)):
            lower.pop()
        lower.append(p)
    # Build upper hull
    upper = []
    for p in reversed(points):
        while((len(upper)>=2) and (_cross(upper[-2],upper[-1],p)<EPS)):
            upper.pop()
        upper.append(p)
    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list.
    return lower[:-1] + upper[:-1]
###############################################
###             Polygon Area                ###
###############################################
def poly_area(v):
    s = 0
    for k in range(len(v)-1):
        s += conj(v[k])*v[k+1]
    return 0.5*s.imag
###############################################
###             Numerical Range Main        ###
###############################################
def nr_main(a):
    # set size and norm
    n,_ = a.shape
    nrm = norm(a,ord='fro')
    # Hermitian test
    err = norm(a - conj(transpose(a)),ord='fro')
    if(err < max(TOL*nrm,TOL)):
        eig = eigvalsh(a)
        ind = argsort(eig)
        eig = eig[ind]
        return [eig[0],eig[-1]], eig
    # Normal test
    err = norm(dot(conj(transpose(a)),a) - dot(a,conj(transpose(a))),ord='fro')
    eig = eigvals(a)
    if(err < max(TOL*nrm,TOL)):
        convHull = cmplxConvHull(eig)
        convHull.append(convHull[0])
        return convHull, eig
    # eigenvalues and inscribed polygon vertices (for non-normal matrices)
    # Caching wrapper for _nr_at(a, ...)
    @lru_cache(maxsize=None)
    def nr_at_fn(angl):
        return _nr_at(a, angl)
    angls = [0, 0.25, 0.5, 0.75, 1]
    p = [nr_at_fn(angl)[1] for angl in angls]
    ind = 0
    for k in range(len(angls)-1):
        ind = _nr_sub(nr_at_fn, angls, p, ind)
    # May not be needed, but doesn't hurt
    nr_at_fn.cache_clear()
    return p, eig

# Function to compute eigenvalue, etc. data for the Hermitian part of a rotation of the matrix
def _nr_at(a,angl):
    # multiply by complex exponential
    a1 = exp(2*pi*1j*angl)*a
    # compute hermitian part
    a2 = (a1 + transpose(conj(a1)))/2
    # compute eigenvalues and eigenvectors of hermitian part
    eigval, eigvec = eigh(a2)
    # sort eigenvalues and return maximum eigenvalue and associated inscribed polygonal vertex
    ind = argsort(eigval)
    eigval = eigval[ind][-1]
    eigvec = eigvec[:,ind][:,-1]
    return eigval, dot(conj(eigvec),dot(a,eigvec))

###############################################
###             Numerical Range Sub         ###
###############################################
def _nr_sub(nr_at_fn,angls,p,ind0):
    a0 = angls[ind0]
    a1 = angls[ind0+1]
    da = a1 - a0
    ax = a1 + da
    e0, p0 = nr_at_fn(a0)
    e1, p1 = nr_at_fn(a1)
    ex, px = nr_at_fn(ax)
    q0 = exp(-2*pi*1j*a0)*(e0+1j*(e0*cos(2*pi*da)-e1)/sin(2*pi*da))
    q1 = exp(-2*pi*1j*a1)*(e1+1j*(e1*cos(2*pi*da)-ex)/sin(2*pi*da))
    area = poly_area([p0,p1,q1,q0,p0])
    # return or sub-divide
    if (area<=TOL2):
        return ind0 + 1
    else:
        am = a0 + da / 2
        em, pm = nr_at_fn(am)
        angls.insert(ind0 + 1, am)
        p.insert(ind0 + 1, pm)
        indm = _nr_sub(nr_at_fn, angls, p, ind0)
        return _nr_sub(nr_at_fn, angls, p, indm)
###############################################
###         Restricted Laplacian            ###
###############################################
def ql(l):
    n, _ = l.shape
    q = zeros((n,n-1),dtype=float)
    for j in range(n-1):
        q[0:j+1,j] = 1
        q[j+1,j] = -(j+1)
        q[:,j] = q[:,j]/norm(q[:,j])
    a = dot(transpose(q),dot(l,q))
    return a
###############################################
###         Restricted Numerical Range      ###
###############################################
def qnr(l):
    return nr_main(ql(l))
###############################################
###             Normality Tests             ###
###############################################
def normality(l):
    # check if l is normal
    ln = False
    nrm = norm(l,ord='fro')
    err = norm(dot(conj(transpose(l)),l) - dot(l,conj(transpose(l))),ord='fro')
    if(err < max(TOL,TOL*nrm)):
        ln = True
    # build a = q^{T}lq
    a = ql(l)
    # check if a is normal
    an = False
    nrm = norm(a,ord='fro')
    err = norm(dot(conj(transpose(a)),a) - dot(a,conj(transpose(a))),ord='fro')
    if(err < max(TOL*nrm,TOL)):
        an = True
    # return
    return ln, an
