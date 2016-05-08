set(GAME_ROOT ${CMAKE_CURRENT_SOURCE_DIR})
set(CORE_ROOT ${GAME_ROOT}/core)
set(CORE_SRC ${CORE_ROOT}/src)

set(
COMMON_FILES

"${CORE_SRC}/screens/test_screen.cpp"

"${CORE_SRC}/<#[game_name_lower]#>.cpp"

# Put your other sources here
#  e.g. "${CORE_SRC}/screens/screen_two.cpp"
#       "${CORE_SRC}/other.cpp"

)
