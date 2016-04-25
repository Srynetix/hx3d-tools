#include "hx3d/window/sdl2/sdl2_application.hpp"
#include "hx3d/window/application_config.hpp"

#include "game/hello.hpp"

using namespace hx3d;
using namespace hx3d::window;

int main(int argc, char** argv) {
  ApplicationConfig config;
  SDL2Application app(config);
  app.start(Make<hello>());

  return 0;
}


