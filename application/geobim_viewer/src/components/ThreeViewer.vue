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
	SpriteMaterial,
	AxesHelper
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
	camera: PerspectiveCamera;
	controls: OrbitControls;
	pLight: PointLight;
	dirLight: DirectionalLight;
	ambLight: AmbientLight;

	needsRerender = 0;

	initScene() {

		this.scene = new Scene();
		this.scene.background = new Color( 0xeeeeee );

		const canvas = document.getElementById( "canvas" );

		this.renderer = new WebGLRenderer( { antialias: false } );
		this.renderer.setPixelRatio( window.devicePixelRatio );
		this.renderer.setSize( canvas!.clientWidth, canvas!.clientHeight );
		this.renderer.setClearColor( 0xd9eefc );
		this.renderer.outputEncoding = sRGBEncoding;
		this.renderer.autoClear = false;

		canvas!.appendChild( this.renderer.domElement );

		this.camera = new PerspectiveCamera( 50, canvas!.clientWidth / canvas!.clientHeight, 2, 30000 );
		this.camera.position.set( 0, 20, 0 );

		this.controls = new OrbitControls( this.camera, this.renderer.domElement );
		this.controls.screenSpacePanning = false;
		// this.controls.enableDamping = true;
		// this.controls.dampingFactor = 0.15;
		this.controls.minDistance = 0;
		this.controls.maxDistance = 18000;
		this.controls.maxPolarAngle = 0.8;
		this.controls.mouseButtons = {
			LEFT: MOUSE.PAN,
			MIDDLE: MOUSE.DOLLY,
			RIGHT: MOUSE.ROTATE
		};
		this.controls.touches = {
			ONE: TOUCH.ROTATE,
			TWO: TOUCH.DOLLY_PAN
		};

		this.controls.addEventListener( "change", () => {

			this.needsRerender = 1;

			this.renderScene();

		} );

        const dirLight = new DirectionalLight( 0xffffff, 0.3 );
		const ambLight = new AmbientLight( 0x404050 );
		this.scene.add( dirLight );
        this.scene.add( ambLight );

		const axesHelper = new AxesHelper( 5 );
		this.scene.add( axesHelper );

		this.needsRerender = 1;

		this.renderScene();
		
	}

	mounted() {

		this.initScene();

	}

	renderScene() {

		requestAnimationFrame( this.renderScene );

		if ( this.needsRerender > 0 ) {

			this.needsRerender --;

			// this.controls.update();
			this.camera.updateMatrixWorld();

			this.renderer.render( this.scene, this.camera );


		}

	}

	loadglTF( url: string ) {

		const loader = new GLTFLoader();
		
		// const isIE11 = !!window.MSInputMethodContext && !!document.documentMode;
		const isIE11 = false;
		
		if (!isIE11) {

			const draco = new DRACOLoader;

			draco.setDecoderPath( 'https://unpkg.com/three@0.126.0/examples/js/libs/draco/gltf/' );
			loader.setDRACOLoader(draco);

		}            
		
		loader.load( url, gltf => {

				this.scene.add(gltf.scene);

				console.log( gltf );

				const createdLines = {};
				const geometryCount = {};

				gltf.scene.traverse((obj) => {
					if (obj.isMesh && obj.geometry) {
						geometryCount[obj.geometry.id] = 1;
					}
				});

				// @todo we'll make this more adaptive and pregenerate the lines in gltf.
				const createLines = Object.keys(geometryCount).length <= 500;
				if (!createLines) {
					console.log("not creating line geometries due to model size");
				}

				gltf.scene.traverse((obj) => {
					if (obj.isMesh && obj.geometry) {
						self.originalMaterials.set(obj.id, obj.material);
						obj.material.side = THREE.DoubleSide;
						obj.material.depthWrite = !obj.material.transparent;

						if (createLines) {
							const edges = undefined;
							if (obj.geometry.id in createdLines) {
								edges = createdLines[obj.geometry.id];
							} else {
								edges = createdLines[obj.geometry.id] = new THREE.EdgesGeometry(obj.geometry);
							}
							const line = new THREE.LineSegments(edges, lineMaterial);
							obj.add(line);
						}                            
					}

					if (obj.name.startsWith("product-")) {
						const id2 = obj.name.substr(8, 36);
						const g = Utils.CompressGuid(id2);
						self.allIds.push(g);
						self.nameToId.set(g, obj.id);
						self.nameToId.set(obj.name, obj.id);
					}
				});

				if (first) {

					const boundingBox = new THREE.Box3();
					boundingBox.setFromObject(scene);
					const center = new THREE.Vector3();
					boundingBox.getCenter(center);
					controls.target = center;
					
					// An initial for viewer distance based on the diagonal so that
					// we have a camera matrix for a more detailed calculation.
					const viewDistance = boundingBox.getSize(new THREE.Vector3()).length();
					camera.position.copy(center.clone().add(
						new THREE.Vector3(0.5, 0.25, 1).normalize().multiplyScalar(viewDistance)
					));
					
					// Make sure all matrices get calculated.
					camera.near = viewDistance / 100;
					camera.far = viewDistance * 100;
					controls.update();
					camera.updateProjectionMatrix();
					camera.updateMatrixWorld();
					
					const fovFactor = Math.tan(camera.fov / 2 / 180 * 3.141592653);
					const outside = 0.;
					
					// Calculate distance between projected bounding box coordinates and view frustrum boundaries
					const largestAngle = 0.;
					for (const i = 0; i < 8; i++) {
						const v = new THREE.Vector3(
							i & 1 ? boundingBox.min.x : boundingBox.max.x,
							i & 2 ? boundingBox.min.y : boundingBox.max.y,
							i & 4 ? boundingBox.min.z : boundingBox.max.z
						);
						v.applyMatrix4(camera.matrixWorldInverse);
						// largestAngle = Math.max(largestAngle, Math.atan2(v.x / camera.aspect, -v.z), Math.atan2(v.y, -v.z));
						outside = Math.max(outside, Math.abs(v.x / camera.aspect) - fovFactor * -v.z, Math.abs(v.y) - fovFactor * -v.z);
						console.log(v.x / camera.aspect, fovFactor * -v.z);
					}
					
					viewDistance += outside * 2;
					
					camera.position.copy(center.clone().add(
						new THREE.Vector3(0.5, 0.25, 1).normalize().multiplyScalar(viewDistance)
					));

					controls.update();
					
					first = false;
				}
				
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
