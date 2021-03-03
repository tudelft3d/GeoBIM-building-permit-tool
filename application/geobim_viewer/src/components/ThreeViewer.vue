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
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js'

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

	loadglTF( url: string ) {

		const loader = new GLTFLoader();
		
		// var isIE11 = !!window.MSInputMethodContext && !!document.documentMode;
		const isIE11 = false;
		
		if (!isIE11) {

			const draco = new DRACOLoader;

			draco.setDecoderPath( 'https://unpkg.com/three@0.126.0/examples/js/libs/draco/gltf/' );
			loader.setDRACOLoader(draco);

		}            
		
		loader.load( url, gltf => {

				console.log( "hoi" );

				this.scene.add(gltf.scene);

				console.log( gltf );

				// var createdLines = {};
				// var geometryCount = {};

				// gltf.scene.traverse((obj) => {
				// 	if (obj.isMesh && obj.geometry) {
				// 		geometryCount[obj.geometry.id] = 1;
				// 	}
				// });

				// // @todo we'll make this more adaptive and pregenerate the lines in gltf.
				// var createLines = Object.keys(geometryCount).length <= 500;
				// if (!createLines) {
				// 	console.log("not creating line geometries due to model size");
				// }

				// gltf.scene.traverse((obj) => {
				// 	if (obj.isMesh && obj.geometry) {
				// 		self.originalMaterials.set(obj.id, obj.material);
				// 		obj.material.side = THREE.DoubleSide;
				// 		obj.material.depthWrite = !obj.material.transparent;

				// 		if (createLines) {
				// 			var edges;
				// 			if (obj.geometry.id in createdLines) {
				// 				edges = createdLines[obj.geometry.id];
				// 			} else {
				// 				edges = createdLines[obj.geometry.id] = new THREE.EdgesGeometry(obj.geometry);
				// 			}
				// 			var line = new THREE.LineSegments(edges, lineMaterial);
				// 			obj.add(line);
				// 		}                            
				// 	}

				// 	if (obj.name.startsWith("product-")) {
				// 		const id2 = obj.name.substr(8, 36);
				// 		const g = Utils.CompressGuid(id2);
				// 		self.allIds.push(g);
				// 		self.nameToId.set(g, obj.id);
				// 		self.nameToId.set(obj.name, obj.id);
				// 	}
				// });

				// if (first) {

				// 	var boundingBox = new THREE.Box3();
				// 	boundingBox.setFromObject(scene);
				// 	var center = new THREE.Vector3();
				// 	boundingBox.getCenter(center);
				// 	controls.target = center;
					
				// 	// An initial for viewer distance based on the diagonal so that
				// 	// we have a camera matrix for a more detailed calculation.
				// 	var viewDistance = boundingBox.getSize(new THREE.Vector3()).length();
				// 	camera.position.copy(center.clone().add(
				// 		new THREE.Vector3(0.5, 0.25, 1).normalize().multiplyScalar(viewDistance)
				// 	));
					
				// 	// Make sure all matrices get calculated.
				// 	camera.near = viewDistance / 100;
				// 	camera.far = viewDistance * 100;
				// 	controls.update();
				// 	camera.updateProjectionMatrix();
				// 	camera.updateMatrixWorld();
					
				// 	var fovFactor = Math.tan(camera.fov / 2 / 180 * 3.141592653);
				// 	var outside = 0.;
					
				// 	// Calculate distance between projected bounding box coordinates and view frustrum boundaries
				// 	var largestAngle = 0.;
				// 	for (var i = 0; i < 8; i++) {
				// 		const v = new THREE.Vector3(
				// 			i & 1 ? boundingBox.min.x : boundingBox.max.x,
				// 			i & 2 ? boundingBox.min.y : boundingBox.max.y,
				// 			i & 4 ? boundingBox.min.z : boundingBox.max.z
				// 		);
				// 		v.applyMatrix4(camera.matrixWorldInverse);
				// 		// largestAngle = Math.max(largestAngle, Math.atan2(v.x / camera.aspect, -v.z), Math.atan2(v.y, -v.z));
				// 		outside = Math.max(outside, Math.abs(v.x / camera.aspect) - fovFactor * -v.z, Math.abs(v.y) - fovFactor * -v.z);
				// 		console.log(v.x / camera.aspect, fovFactor * -v.z);
				// 	}
					
				// 	viewDistance += outside * 2;
					
				// 	camera.position.copy(center.clone().add(
				// 		new THREE.Vector3(0.5, 0.25, 1).normalize().multiplyScalar(viewDistance)
				// 	));

				// 	controls.update();
					
				// 	first = false;
				// }
				
				// self.fire("loaded");
			},

			// called while loading is progressing
			function(xhr) {
				console.log((xhr.loaded / xhr.total * 100) + '% loaded');
			},

			// called when loading has errors
			function(error) {
				console.log('An error happened', error);
			}
		);

	}

}

</script>

<style scoped>
#canvas {
  width: 100%;
  height: 100%;
}
</style>
