#include "hx3d/window/sdl2/sdl2_application.hpp"
#include "game/<#[game_name_lower]#>.hpp"

using namespace hx3d;
using namespace hx3d::window;

int main(int argc, char** argv) {

  ApplicationConfig config;
  SDL2Application app(config);
  app.start(Make<<#[game_name]#>>());

  return 0;
}
