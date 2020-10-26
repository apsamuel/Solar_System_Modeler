# Solar System Model

## Goals

* To render a (semi)realistic model of our solar systems major bodies (the sun, the observed planets, the natural planetary satellites [**a/k/a** the moons])
* Self-contained workflow
  * acquire required data without external inputs


## Data Sources

* Planetary Data - [The Solar System OpenData](https://api.le-systeme-solaire.net/swagger/)
* Formula

  * >each planet's orbit about the Sun is an ellipse. The Sun's center is always located at one focus of the orbital ellipse. The Sun is at one focus. The planet follows the ellipse in its orbit, meaning that the planet to Sun distance is constantly changing as the planet goes around its orbit.
  * >citation [keplers laws](https://solarsystem.nasa.gov/resources/310/orbits-and-keplers-laws/#:~:text=Kepler's%20Third%20Law%3A%20the%20squares,the%20radius%20of%20its%20orbit)
    * **Deriving the `semi-minor-axis` from `semi-major-axis` & `eccentrity` values**

      * >The eccentricity (e) of an ellipse is a number that quantifies how elongated the ellipse is. It equals 1 - (perihelion)/(semi-major axis). Circles have an eccentricity = 0; very long and skinny ellipses have an eccentricity close to 1 (a straight line has an eccentricity = 1). The skinniness an ellipse is specified by the semi-minor axis. It equals the semi-major axis × Sqrt[(1 - e2)]. 

      * >citation: [Astronomy Notes](hhttps://www.astronomynotes.com/history/s7.htm)

        * ![formula](https://latex.codecogs.com/svg.latex?semiMinorAxis=semiMajorAxis*\sqrt{(1-e^2)})

  * **Angular Rotation Calculations**

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; From a top down view, given the imaginary lines drawn by the distances between objects:
  * a) `orbitingBody(x,y)` <-> `radiusLen(0,y)` (*side a*)
    * the distance from (0,0) to (0,`planetsAverageRadius`)
  * b) `sunCenter(0,0)` <-> `orbitingBody(x,y)` (*side b*) 
    * the distance from (0,0) to the `orbitingBody`
  * c) `sunCenter(0,0)` <-> `radiusLen(0,y)` (*side c*)

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ![triangle](https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Triangle_with_notations_2.svg/2880px-Triangle_with_notations_2.svg.png)

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Angle(alpha) is derived by:
  * not if:
    * `y==0` && `x==semiMajorAxis` || `y==0` && `x==-semiMajorAxis` 
    * `y==semiMinorAxis` && `x==0` || `y==-semiMinorAxis` && `x==0`
  * if [ ( `x > 0` && `x < semiMajorAxis` ) && ( `y > 0` && `y < semiMinorAxis` )] (*Quadrant **I***)
    * ![formula](https://latex.codecogs.com/svg.latex?\alpha=\frac{{b^2+c^2-a^2}}{2*b*c})
  * if [ ( `x > -semiMajorAxis` && `x < 0` ) && `y > 0` && `y < semiMinorAxis` ] (*Quadrant **II***)
    * ![formula](https://latex.codecogs.com/svg.latex?\alpha=\frac{{a^2+c^2-b^2}}{2*a*c})
  * if [ ( `x > -semiMajorAxis` && `x < 0` ) && `y > 0` && `y < semiMinorAxis` ] (*Quadrant **III***) 
    * ![formula](https://latex.codecogs.com/svg.latex?\alpha=\frac{{a^2+b^2-c^2}}{2*a*b})
  * if [ ( `x > -semiMajorAxis` && `x < 0` ) && `y > 0` && `y < semiMinorAxis` ] (*Quadrant **IV***)
    * ![formula](https://latex.codecogs.com/svg.latex?\alpha=\frac{{a^2+b^2-c^2}}{2*a*b})