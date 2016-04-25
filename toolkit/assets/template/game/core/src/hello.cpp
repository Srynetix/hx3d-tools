#include "game/hello.hpp"

#include "game/screens/test_screen.hpp"

#include "hx3d/utils/assets.hpp"

#include "hx3d/core/core.hpp"
#include "hx3d/window/events.hpp"

using namespace hx3d;

void hello::create() {

  /** Want to load a texture ?
    *   Core::Assets()->create<Texture>("texture_name", "textures/here.png")
    */

  Core::Events()->emulateTouchWithMouse(true);

  this->setScreen(Make<TestScreen>());
}

