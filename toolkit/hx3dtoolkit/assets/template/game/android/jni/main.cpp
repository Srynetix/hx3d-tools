#include "hx3d/window/application.hpp"
#include "game/<#[game_name_lower]#>.hpp"

using namespace hx3d;
using namespace hx3d::window;

int main(int argc, char** argv) {

  ApplicationConfig config;
  Application app(config);
  app.start(Make<<#[game_name]#>>());

  return 0;
}
