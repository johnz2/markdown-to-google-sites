# ABEngine

ABEngine is used in MetalStorm: Wingman, MetalStorm 2: Aces, and Racecraft.

## Contacts

*   Aces: John Jensen, <john@z2live.com>
*   Racecraft: Marcel Barker, <marcel@z2live.com>
*   Z2Live: Ryan Murphy, <ryan@z2live.com>

## Code Standards

Please adopt the [programming conventions we use][code-standards] for the engine.

[code-standards]: https://sites.google.com/a/z2live.com/metalstorm/engineering/code-standards
    "ABEngine Code Standards"

# Engine Changelog

Initially, the engine changelog is grouped into major releases but if since we
are to work on the `master` branch at the same time, we may have to use ongoing
changelogs to communicate API change going forward.

This changelog is formatted with [Markdown][markdown-syntax] and line lengths
shouldn't extend past 80 characters to allow for easy reading in the terminal
and in GitX's commit history.

[markdown-syntax]: http://daringfireball.net/projects/markdown/basics
    "Basic Markdown Syntax"
    

## Mar '12: Early Aces development

*   (forthcoming)


## Feb '12: Merge BSG into MSW engine

Notes from John Jensen.

### Major changes

+   There is now an engine Xcode project (`abengine.xcodeproj`), which should
    be used instead of including engine code in product targets directly.

+   A new resource management system is a centralized facility to load content.

+   New utility functionality such as logging and debugging variables.

### Work in development

+   A new entity and component system that will compile side-by-side with
    existing entity system.

### New Resource Manager

*   Breaking API change: 
    ... More details ...

### Entity system

*   Breaking API change: Prefab and entity creation was changed to support the
    resource manager. `ABEntitySystem` was refactored to read and flow more
    naturally.
    
    ... More details ...
    
### Debug
 
+   Moved to `z2assert(expr)`. This assert is continuable and, like the
    deprecated `DebugAssert()`, compiles out in `RELEASE` builds.

+   Added `AB_LOG` logging facility. See `ABLogging.h`.

+   DEBUG & TWEAK variables

+   Draw 2d graphs with `ABDebugSystem`, useful for FPS or memory graphs.

+   `ABDebugHUD`, with support for toggling different plug-ins to enable or
    disable certain development tools.

+   `INSTRUMENT_FUNCTION()` and `INSTRUMENT_SCOPE("foo")` added and integrated
    with above performance monitoring systems.

### Math

*   Breaking API change: An `ABVector3`'s magnitude is now retrievable by
    `ABVector3::magnitude()` and `ABVector3::magnitudeSquared()`.
    `ABVector3::size()` and `ABVector3::magnitudeNoSqrt()` have been deleted.

+   To create an uninitialized `ABVector3` or `ABQuaternion`, one can now call
    the following constructor:

        ABVector3 emptyVector(NoInit);
        ABQuaternion emptyQuat = ABQuaternion(NoInit);

  Asserts will likely fire if you don't later initialize the values.
  
+   `ABVector3::normalize()` and `ABQuaternion::normalize()` has been optimized
    to not do a conditional check for the zero vector case.

+   Bullet Physics now uses `z2assert`.

## Dec '11: BSG Engine Improvements

Notes from Marcel Barker.

### Rendering

#### ABRenderModuleOpenGLES1

*   Added support for floating point UV's – this code is wrapped with the
    define `AB_USE_SHORT_UV`.

#### ABRenderModuleOpenGLES2

*   Added two more texture uniforms in the shader. Went from having one primary
    and one auxiliary texture to having four optional textures per material.

*   In `drawModel`, calls the material's hint function when setting textures.

*   Vertex attribute pointers were handled in various locations at a low level,
    added a centralized attribute description.

*   Added vertex colours.

*   Implemented `drawSpritesAsQuads` for ES2.

*   Generating vertex array objects in ES2.

*   Hooked up render debug.

#### ABMesh

*   Change `ABUniqueVertex` tags from `short` to `unsigned short`, as it was
    causing bugs.

*   `secondCoords` were causing bugs — removed.

#### ABVertexData

*   Adding means of gathering data about vertices.


#### EAGLView
*   Changed the frame interval from 2 to 1. this can be removed.

### POD Components

#### ScenePODComponent

This component loads a .pod file and renders it. It doesn't require a render
component or a material component, as this data is in the .pod file directly.
In its current state, this component should probably be in the RaceCraft
project rather than Engine, however it could be cleaned up and made more
generic. The major issue that makes it game-specific is its knowledge of
material prefixes and texture suffixes. 

#### CameraPODComponent

This component takes camera animation data in a .pod file and animates the game
camera accordingly.

### UI HTML Bindings

Affected files:

    UiJsBinding.h/.mm
    ViewController.h/.mm (Game project)
    ViewController.xib (Game project)
    GameViewiPad.xib (Editor project)
    ABOSXViewGame.h/.mm (Editor project)
    mso_uijs.js

For the affected .xib files, we added a Web View as a sibling which sits on top
of the existing GLView. This was bound to the `uiView` member of
`ViewController` (Game) or `ABOSXViewGame` (Editor). 

`UiJsBinding` is the class responsible for handling the communication between
HTML and the game. We initialize the system by setting the `UiJsBinding`'s web
view in `ViewController`'s `setEngine` function.

The Objective-C class that wishes to receive game messages registers a selector
with `UiJsBinding`.

	[UiJsBinding setCallback:@selector(startGas:) withReceiver:self forHook:@"startGas"];
	
Calling JavaScript functions from the game is also done through `UiJsBinding`.

	[UiJsBinding callScriptFunction:@"setNitroUses" withArgs:args];

Communication from the game to HTML is done through the web view's 
`stringByEvaluatingJavaScriptFromString` function, which calls the specified
JavaScript function. Communication from HTML to the game is done through
intercepted navigation messages, via `shouldStartLoadWithRequest` on iOS and 
`decidePolicyForNavigationAction` on OS X. If the navigation URL begins with
the tag `uijsmsg`, the request is interpreted as a game message. `mso_uijs.js`
contains the function gameMsg which wraps this functionality.

    function gameMsg( message, args ) {
        window.location = '"uijsmsg":{"msg":"' + message + '","args":' + args + '}';
    }

### Bullet Physics

Integration should be simple – the only change to existing code was to add
`PhysicsManager` to the `ABEngine`.

Changes made to Bullet source:

*   `btRaycastVehicle` was made virtual, to allow us to create a custom
    `btRacecraftRaycastVehicle`

*   shapes were made changeable after creation

*   debug renderer was fixed to render imported convex hulls

`PhysicsManager` is an `ABSystem` which handles creation and destruction of
rigid bodies, and also sets up the dynamics world, constraints solver, etc.
It also does the debug rendering.

The `BulletPhysicsRigidBodyComponent` is an `ABComponent` which handles shape,
mass, friction, restitution, and other physics properties for a physics object.
It can import `.bullet` files or be a box, sphere, or capsule.

Custom collision with callbacks is currently a work in progress.

###Utilities

A couple of utility classes have been added that you may find useful.

+   `ABSpline` is a spline class which can be interpreted as either Catmull
    Rom, B-Splines, or linear.

+   `ABEvent` has a simple templated event system.


## Oct '11: Initial Refactor: MSW handoff to BSG

Notes from Josh Rosen.

*   `ABEntity` is now `Engine::Entity`.

*   `ABComponent` is now `Engine::Component`.

*   The sprite emitter system is now designed to work with both components
    (`SpriteEmitterComponent`) and entities (`ABSpriteEmitter`) through an
    interface. However, the `ABSpriteEmitter` needs to be set up to provide
    the implementation for the interface.

*   Some of the `virtual` `Entity` runloop methods have been renamed (e.g.
    `update`, `serialize`, etc). Unfortunately, C++ doesn't have a good way of
    warning us about methods that are supposed to be overriding a superclass'
    method, but aren't.