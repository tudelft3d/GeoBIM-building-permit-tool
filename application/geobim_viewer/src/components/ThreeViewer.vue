<template>
  <div id="canvas" />
</template>

<script lang="ts">

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

import Vue from 'vue'
import Component from 'vue-class-component'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

@Component({

})

export default class ThreeViewer extends Vue {

	scene: Scene;
	renderer: WebGLRenderer;

	initScene() {

		this.scene = new Scene();
		this.scene.background = new Color( 0xffffff );

		const canvas = document.getElementById( "canvas" );

		this.renderer = new WebGLRenderer( { antialias: false } );
		this.renderer.setPixelRatio( window.devicePixelRatio );
		this.renderer.setSize( canvas!.clientWidth, canvas!.clientHeight );
		this.renderer.setClearColor( 0xd9eefc );
		this.renderer.outputEncoding = sRGBEncoding;
		this.renderer.autoClear = false;

		canvas!.appendChild( this.renderer.domElement );

		// this.renderer.render( this.scene, this.camera );
		
	}

	mounted() {

		this.initScene();

	}

}

</script>

<style scoped>
#canvas {
  width: 100%;
  height: 100%;
}
</style>
