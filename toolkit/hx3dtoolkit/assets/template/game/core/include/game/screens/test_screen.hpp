#ifndef GAME_SCREENS_TESTSCREEN
#define GAME_SCREENS_TESTSCREEN

#include "hx3d/window/screen.hpp"

#include "hx3d/graphics/shader.hpp"
#include "hx3d/graphics/batch.hpp"

#include "hx3d/graphics/cameras/perspective_camera.hpp"

#include "hx3d/graphics/geometries/star_geometry.hpp"
#include "hx3d/graphics/geometries/origin_geometry.hpp"

using namespace hx3d;
using namespace hx3d::graphics;
using namespace hx3d::window;

class TestScreen: public Screen {

public:
  TestScreen();

  virtual void update(float delta) override;
  virtual void render() override;
  virtual void resize(int width, int height) override;

private:
  Ptr<Shader> shader;

  PerspectiveCamera camera;
  Batch batch;

  Mesh star;
  Mesh origin;

  float angle;
};

#endif
