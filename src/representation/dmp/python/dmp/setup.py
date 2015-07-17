def cython_path(filename):
    if "setup.pyc" in __file__:
        return __file__.replace("setup.pyc", filename)
    else:
        return __file__.replace("setup.py", filename)


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration("dmp", parent_package, top_path)
    try:
        import build_info
    except ImportError:
        build_info = None
    if build_info is None:
        config.set_options(ignore_setup_xxx_py=True,
                           assume_default_configuration=True,
                           delegate_options_to_subpackages=True,
                           quiet=True)
        return config

    from Cython.Build import cythonize
    import numpy

    cythonize(cython_path("dmp_cpp.pyx"), language="c++")

    # CMake outputs multiple include dirs separated by ";"
    # but the setup scripts needs it as list => split it
    config.add_extension(
        'dmp_cpp',
        sources=["dmp_cpp.cpp"],  # Generated by cythonize
        include_dirs=["../src",
                      numpy.get_include(),
                      build_info.EIGEN_INCLUDE_DIR,
                      build_info.YAML_INCLUDE_DIR,
                      build_info.LIB_MANAGER_INCLUDE_DIRS,
                      build_info.BOLERO_INCLUDE_DIRS.split(";")],
        libraries=["dmp_cpp", "yaml-cpp"],
        library_dirs=[build_info.DMP_LIBRARY_DIR, build_info.YAML_LIBRARY_DIR],
        define_macros=[("NDEBUG",)],
        extra_compile_args=["-O3"],
    )

    cythonize(cython_path("rigid_body_dmp_cpp.pyx"), language="c++")

    config.add_extension(
        'rigid_body_dmp_cpp',
        sources=["rigid_body_dmp_cpp.cpp"],  # Generated by cythonize
        include_dirs=["../src",
                      numpy.get_include(),
                      build_info.EIGEN_INCLUDE_DIR,
                      build_info.YAML_INCLUDE_DIR,
                      build_info.LIB_MANAGER_INCLUDE_DIRS,
                      build_info.BOLERO_INCLUDE_DIRS.split(";")],
        libraries=["rigid_body_dmp_cpp", "yaml-cpp"],
        library_dirs=[build_info.DMP_LIBRARY_DIR, build_info.YAML_LIBRARY_DIR],
        define_macros=[("NDEBUG",)],
        extra_compile_args=["-O3"],
    )

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
