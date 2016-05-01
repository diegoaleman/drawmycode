'''OpenGL extension ARB.vertex_shader

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.vertex_shader to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension adds programmable vertex level processing to OpenGL. The
	application can write vertex shaders in a high level language as defined
	in the OpenGL Shading Language specification. The language itself is not
	discussed here. A vertex shader replaces the transformation, texture
	coordinate generation and lighting parts of OpenGL, and it also adds
	texture access at the vertex level. Furthermore, management of vertex
	shader objects and loading generic attributes are discussed. A vertex
	shader object, attached to a program object, can be compiled and linked
	to produce an executable that runs on the vertex processor in OpenGL.
	This extension also defines how such an executable interacts with the
	fixed functionality vertex processing of OpenGL 1.4.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/vertex_shader.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.ARB.vertex_shader import *
from OpenGL.raw.GL.ARB.vertex_shader import _EXTENSION_NAME

def glInitVertexShaderARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

glVertexAttrib1fvARB=wrapper.wrapper(glVertexAttrib1fvARB).setInputArraySize(
    'v', 1
)
glVertexAttrib1svARB=wrapper.wrapper(glVertexAttrib1svARB).setInputArraySize(
    'v', 1
)
glVertexAttrib1dvARB=wrapper.wrapper(glVertexAttrib1dvARB).setInputArraySize(
    'v', 1
)
glVertexAttrib2fvARB=wrapper.wrapper(glVertexAttrib2fvARB).setInputArraySize(
    'v', 2
)
glVertexAttrib2svARB=wrapper.wrapper(glVertexAttrib2svARB).setInputArraySize(
    'v', 2
)
glVertexAttrib2dvARB=wrapper.wrapper(glVertexAttrib2dvARB).setInputArraySize(
    'v', 2
)
glVertexAttrib3fvARB=wrapper.wrapper(glVertexAttrib3fvARB).setInputArraySize(
    'v', 3
)
glVertexAttrib3svARB=wrapper.wrapper(glVertexAttrib3svARB).setInputArraySize(
    'v', 3
)
glVertexAttrib3dvARB=wrapper.wrapper(glVertexAttrib3dvARB).setInputArraySize(
    'v', 3
)
glVertexAttrib4fvARB=wrapper.wrapper(glVertexAttrib4fvARB).setInputArraySize(
    'v', 4
)
glVertexAttrib4svARB=wrapper.wrapper(glVertexAttrib4svARB).setInputArraySize(
    'v', 4
)
glVertexAttrib4dvARB=wrapper.wrapper(glVertexAttrib4dvARB).setInputArraySize(
    'v', 4
)
glVertexAttrib4ivARB=wrapper.wrapper(glVertexAttrib4ivARB).setInputArraySize(
    'v', 4
)
glVertexAttrib4bvARB=wrapper.wrapper(glVertexAttrib4bvARB).setInputArraySize(
    'v', 4
)
glVertexAttrib4ubvARB=wrapper.wrapper(glVertexAttrib4ubvARB).setInputArraySize(
    'v', 4
)
glVertexAttrib4usvARB=wrapper.wrapper(glVertexAttrib4usvARB).setInputArraySize(
    'v', 4
)
glVertexAttrib4uivARB=wrapper.wrapper(glVertexAttrib4uivARB).setInputArraySize(
    'v', 4
)
glVertexAttrib4NbvARB=wrapper.wrapper(glVertexAttrib4NbvARB).setInputArraySize(
    'v', 4
)
glVertexAttrib4NsvARB=wrapper.wrapper(glVertexAttrib4NsvARB).setInputArraySize(
    'v', 4
)
glVertexAttrib4NivARB=wrapper.wrapper(glVertexAttrib4NivARB).setInputArraySize(
    'v', 4
)
glVertexAttrib4NubvARB=wrapper.wrapper(glVertexAttrib4NubvARB).setInputArraySize(
    'v', 4
)
glVertexAttrib4NusvARB=wrapper.wrapper(glVertexAttrib4NusvARB).setInputArraySize(
    'v', 4
)
glVertexAttrib4NuivARB=wrapper.wrapper(glVertexAttrib4NuivARB).setInputArraySize(
    'v', 4
)
# INPUT glVertexAttribPointerARB.pointer size not checked against 'size,type,stride'
glVertexAttribPointerARB=wrapper.wrapper(glVertexAttribPointerARB).setInputArraySize(
    'pointer', None
)
glGetActiveAttribARB=wrapper.wrapper(glGetActiveAttribARB).setOutput(
    'length',size=(1,),orPassIn=True
).setOutput(
    'name',size=lambda x:(x,),pnameArg='maxLength',orPassIn=True
).setOutput(
    'size',size=(1,),orPassIn=True
).setOutput(
    'type',size=(1,),orPassIn=True
)
glGetVertexAttribdvARB=wrapper.wrapper(glGetVertexAttribdvARB).setOutput(
    'params',size=(4,),orPassIn=True
)
glGetVertexAttribfvARB=wrapper.wrapper(glGetVertexAttribfvARB).setOutput(
    'params',size=(4,),orPassIn=True
)
glGetVertexAttribivARB=wrapper.wrapper(glGetVertexAttribivARB).setOutput(
    'params',size=(4,),orPassIn=True
)
glGetVertexAttribPointervARB=wrapper.wrapper(glGetVertexAttribPointervARB).setOutput(
    'pointer',size=(1,),orPassIn=True
)
### END AUTOGENERATED SECTION
from OpenGL._bytes import bytes, _NULL_8_BYTE, as_8_bit
from OpenGL.lazywrapper import lazy as _lazy
from OpenGL.GL.ARB.shader_objects import glGetObjectParameterivARB

base_glGetActiveAttribARB = glGetActiveAttribARB
def glGetActiveAttribARB(program, index):
    """Retrieve the name, size and type of the uniform of the index in the program"""
    max_index = int(glGetObjectParameterivARB( program, GL_OBJECT_ACTIVE_ATTRIBUTES_ARB ))
    length = int(glGetObjectParameterivARB( program, GL_OBJECT_ACTIVE_ATTRIBUTE_MAX_LENGTH_ARB))
    if index < max_index and index >= 0 and length > 0:
        name = ctypes.create_string_buffer(length)
        size = arrays.GLintArray.zeros( (1,))
        gl_type = arrays.GLuintArray.zeros( (1,))
        base_glGetActiveAttribARB(program, index, length, None, size, gl_type, name)
        return name.value, size[0], gl_type[0]
    raise IndexError('index out of range from zero to %i' % (max_index - 1, ))
glGetActiveAttribARB.wrappedOperation = base_glGetActiveAttribARB

@_lazy( glGetAttribLocationARB )
def glGetAttribLocationARB( baseOperation, program, name ):
    """Check that name is a string with a null byte at the end of it"""
    if not name:
        raise ValueError( """Non-null name required""" )
    name = as_8_bit( name )
    if name[-1] != _NULL_8_BYTE:
        name = name + _NULL_8_BYTE
    return baseOperation( program, name )
