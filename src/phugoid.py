# Script per tracciare la traiettoria di volo del fugoide utilizzando il modello di Lanchester.
# Utilizza la convenzione dei segni e le formule fornite da Milne-Thomson (1958).

import numpy
from matplotlib import pyplot

numpy.seterr(all='ignore')
'''
Guarda http://docs.scipy.org/doc/numpy/reference/generated/numpy.seterr.html per comprendere meglio.
ignora gli errori di over/underflow che compaiono nella funzione radius_of_curvature
'''

def radius_of_curvature(z, zt, C):
    """Restituisce il raggio di curvatura della traiettoria di volo in qualsiasi punto.
    
    Parametri
    ---------
    z : float
        profondità attuale al di sotto della linea orizzontale di riferimento.
    zt : float
        profondità iniziale al di sotto della linea orizzontale di riferimento.
    C : float
        costante di integrazione.

    Return
    -------
    radius : float
        raggio di curvatura.
    """
    return zt / (1./3. - C/2.*(zt/z)**1.5)

def rotate(x, z, xCenter, zCenter, angle):
    """Restituisce la nuova posizione del punto.

    Parametri
    ---------
    x : float
        precedente posizione x del punto.
    z : float
        precedente posizione z del punto.
    xCenter : float
        posizione x del centro di rotazione.
    zCenter : float
        posizione z del centro di rotazione.
    angle : float
        angolo di rotazione.

    Returns
    -------
    xCenter_new : float
        nuova posizione x del centro di rotazione.
    zCenter_new : float
        nuova posizione z del centro di rotazione.
    """
    dx = x - xCenter
    dz = z - zCenter
    # le seguenti formule tengono conto dell'orientamento degli assi
    xNew = dx*numpy.cos(angle) + dz*numpy.sin(angle)
    zNew = -dx*numpy.sin(angle) + dz*numpy.cos(angle)
    return xCenter + xNew, zCenter + zNew

def plot_flight_path(zt, z0, theta0):
    """Traccia la traiettoria di volo.

    Parametri
    ---------
    zt : float
        altezza di assetto dell'aliante.
    z0 : float
        altezza iniziale dell'aliante.
    theta0 : float
        orientamento iniziale della vela.

    Returns
    -------
    None : None
    """
    # array per memorizzare le coordinate della traiettoria di volo
    N = 1000
    z = numpy.zeros(N)
    x = numpy.zeros(N)

    # stabilire le condizioni iniziali
    z[0] = z0
    x[0] = 0.
    theta = theta0

    # calcolare la costante C
    C = (numpy.cos(theta) - 1./3.*z[0]/zt)*(z[0]/zt)**.5
    # distanza incrementale lungo la traiettoria di volo
    ds = 1.
        
    # ottenere le coordinate della curva
    for i in range(1,N):
        # segno meno per la seconda coordinata perché l'asse z punta verso il basso
        normal = numpy.array([numpy.cos(theta+numpy.pi/2.), -numpy.sin(theta+numpy.pi/2.)])
        R = radius_of_curvature(z[i-1], zt, C)
        center = numpy.array([x[i-1]+normal[0]*R, z[i-1]+normal[1]*R])
        dtheta = ds/R
        x[i], z[i] = rotate(x[i-1], z[i-1], center[0], center[1], dtheta)
        theta = theta + dtheta

    # generazione della traiettoria
    pyplot.figure(figsize=(10,6))
    pyplot.plot(x, -z, color = 'k', ls='-', lw=2.0, label="$z_t=\ %.1f,\\,z_0=\ %.1f,\\,\\theta_0=\ %.2f$" % (zt, z[0], theta0))
    pyplot.axis('equal')
    pyplot.title("Flight path for $C$ = %.3f" % C, fontsize=18)
    pyplot.xlabel("$x$", fontsize=18)
    pyplot.ylabel("$z$", fontsize=18)
    pyplot.legend()
    pyplot.show()

# End of File