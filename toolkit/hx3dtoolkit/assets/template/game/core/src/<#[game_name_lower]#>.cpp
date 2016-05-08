#include "game/<#[game_name_lower]#>.hpp"

#include "game/screens/test_screen.hpp"

#include "hx3d/utils/assets.hpp"

#include "hx3d/core/core.hpp"
#include "hx3d/window/events.hpp"

using namespace hx3d;

void <#[game_name]#>::create() {

  /** Want to load a texture ?
    *   Core::Assets()->create<Texture>("texture_name", "textures/here.png")
    */

  Core::Events()->emulateTouchWithMouse(true);

  this->setScreen(Make<TestScreen>());
}
