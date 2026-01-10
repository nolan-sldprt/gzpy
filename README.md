# gzpy

A Python library to compute and analyze GZ curves (stability curves) for marine vessels.


## Conventions

### Coordinate System

This package assumes right-handed coordinates and the following conventions,
- the $x$-axis corresponds to surge (roll axis),
- the $y$-axis corresponds to sway (pitch axis), and
- the $z$-axis corresponds to heave (yaw axis)

Because of the right-handed coordinate system,
- $+x$ indicates moving forward,
- $+y$ indicates moving towards port, and
- $+z$ indicates increasing elevation

### Center of Mass (COM)

COM location $(x,y,z)$ must be supplied relative to the origin of the mesh.

### Units

All arguments must be given in SI units.


## Information

### License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.


### Citation

If you use ```gzpy``` in your work, please cite it as below:

```BibTex
@software{gzpy,
    author = {Cain, Nolan},
    license = {Apache-2.0},
    title = {{gzpy}},
    url = {https://github.com/nolan-sldprt/gzpy},
    version = {0.1.0},
}
```
