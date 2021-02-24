<template>
  <div id="canvas" />
</template>

<script>
import {
	Scene,
	Color,
	FogExp2,
	WebGLRenderer,
	sRGBEncoding,
	PerspectiveCamera,
	Group,
	Box3,
	DirectionalLight,
	PointLight,
	AmbientLight,
	Vector2,
	Vector3,
	Raycaster,
	MOUSE,
	TOUCH,
	ShaderMaterial,
	ShaderLib,
	UniformsUtils,
	TextureLoader,
	Sprite,
	SpriteMaterial
} from 'three';

import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

export default {
	name: 'ThreeViewer',
}
</script>

<style scoped>
#canvas {
  width: 100%;
  height: 100%;
}
</style>
