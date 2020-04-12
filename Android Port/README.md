# QChat - Android

The file Structure for the QChat Android app is as follows: 

```
├───Executable APK
└───QChat
    ├───.gradle
    │   ├───5.6.4
    │   │   ├───executionHistory
    │   │   ├───fileChanges
    │   │   ├───fileContent
    │   │   ├───fileHashes
    │   │   ├───javaCompile
    │   │   └───vcsMetadata-1
    │   ├───buildOutputCleanup
    │   └───vcs-1
    ├───.idea
    │   ├───caches
    │   ├───codeStyles
    │   └───libraries
    ├───app
    │   ├───build
    │   │   ├───generated
    │   │   │   ├───ap_generated_sources
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───res
    │   │   │   │   ├───pngs
    │   │   │   │   │   └───debug
    │   │   │   │   │       ├───drawable-anydpi-v21
    │   │   │   │   │       ├───drawable-hdpi
    │   │   │   │   │       ├───drawable-ldpi
    │   │   │   │   │       ├───drawable-mdpi
    │   │   │   │   │       ├───drawable-xhdpi
    │   │   │   │   │       ├───drawable-xxhdpi
    │   │   │   │   │       └───drawable-xxxhdpi
    │   │   │   │   └───resValues
    │   │   │   │       └───debug
    │   │   │   └───source
    │   │   │       └───buildConfig
    │   │   │           └───debug
    │   │   │               └───com
    │   │   │                   └───example
    │   │   │                       └───qchat
    │   │   ├───intermediates
    │   │   │   ├───annotation_processor_list
    │   │   │   │   └───debug
    │   │   │   ├───apk_list
    │   │   │   │   └───debug
    │   │   │   ├───blame
    │   │   │   │   └───res
    │   │   │   │       └───debug
    │   │   │   │           ├───multi-v2
    │   │   │   │           └───single
    │   │   │   ├───bundle_manifest
    │   │   │   │   └───debug
    │   │   │   │       └───bundle-manifest
    │   │   │   ├───compatible_screen_manifest
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───compile_and_runtime_not_namespaced_r_class_jar
    │   │   │   │   └───debug
    │   │   │   ├───data_binding_layout_info_type_merge
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───dex
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───dex_archive_input_jar_hashes
    │   │   │   │   └───debug
    │   │   │   ├───duplicate_classes_check
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───external_libs_dex
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───external_libs_dex_archive
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───incremental
    │   │   │   │   ├───debug-mergeJavaRes
    │   │   │   │   │   └───zip-cache
    │   │   │   │   ├───debug-mergeNativeLibs
    │   │   │   │   │   └───zip-cache
    │   │   │   │   ├───mergeDebugAssets
    │   │   │   │   ├───mergeDebugJniLibFolders
    │   │   │   │   ├───mergeDebugResources
    │   │   │   │   │   ├───merged.dir
    │   │   │   │   │   │   └───values
    │   │   │   │   │   └───stripped.dir
    │   │   │   │   ├───mergeDebugShaders
    │   │   │   │   ├───packageDebug
    │   │   │   │   │   └───tmp
    │   │   │   │   │       └───debug
    │   │   │   │   │           └───zip-cache
    │   │   │   │   └───processDebugResources
    │   │   │   ├───instant_app_manifest
    │   │   │   │   └───debug
    │   │   │   ├───javac
    │   │   │   │   └───debug
    │   │   │   │       └───classes
    │   │   │   │           └───com
    │   │   │   │               └───example
    │   │   │   │                   └───qchat
    │   │   │   ├───manifest_merge_blame_file
    │   │   │   │   └───debug
    │   │   │   ├───merged_assets
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───merged_java_res
    │   │   │   │   └───debug
    │   │   │   ├───merged_jni_libs
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───merged_manifests
    │   │   │   │   └───debug
    │   │   │   ├───merged_native_libs
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───merged_shaders
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───metadata_feature_manifest
    │   │   │   │   └───debug
    │   │   │   │       └───metadata-feature
    │   │   │   ├───mixed_scope_dex_archive
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───navigation_json
    │   │   │   │   └───debug
    │   │   │   ├───processed_res
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───project_dex_archive
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   │           └───com
    │   │   │   │               └───example
    │   │   │   │                   └───qchat
    │   │   │   ├───res
    │   │   │   │   └───merged
    │   │   │   │       └───debug
    │   │   │   ├───runtime_symbol_list
    │   │   │   │   └───debug
    │   │   │   ├───shader_assets
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───stripped_native_libs
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───sub_project_dex_archive
    │   │   │   │   └───debug
    │   │   │   │       └───out
    │   │   │   ├───symbol_list_with_package_name
    │   │   │   │   └───debug
    │   │   │   └───validate_signing_config
    │   │   │       └───debug
    │   │   │           └───out
    │   │   ├───outputs
    │   │   │   ├───apk
    │   │   │   │   └───debug
    │   │   │   └───logs
    │   │   └───tmp
    │   │       └───compileDebugJavaWithJavac
    │   ├───libs
    │   └───src
    │       ├───androidTest
    │       │   └───java
    │       │       └───com
    │       │           └───example
    │       │               └───qchat
    │       ├───main
    │       │   ├───java
    │       │   │   └───com
    │       │   │       └───example
    │       │   │           └───qchat
    │       │   └───res
    │       │       ├───drawable
    │       │       ├───drawable-v24
    │       │       ├───layout
    │       │       ├───mipmap-anydpi-v26
    │       │       ├───mipmap-hdpi
    │       │       ├───mipmap-mdpi
    │       │       ├───mipmap-xhdpi
    │       │       ├───mipmap-xxhdpi
    │       │       ├───mipmap-xxxhdpi
    │       │       └───values
    │       └───test
    │           └───java
    │               └───com
    │                   └───example
    │                       └───qchat
    └───gradle
        └───wrapper

```
