[app]
title = YouTube Hidden Browser
package.name = youtubehiddenbrowser
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,requests,beautifulsoup4,selenium,webdriver-manager,plyer
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.arch = arm64-v8a
android.accept_sdk_license = True
android.gradle_dependencies = 'androidx.webkit:webkit:1.4.0'
android.add_compile_options = org.gradle.jvmargs=-Xmx2048m
android.add_gradle_repositories = mavenCentral()
android.add_gradle_dependencies = 'androidx.webkit:webkit:1.4.0'
android.add_aars = ~/.gradle/caches/modules-2/files-2.1/androidx.webkit/webkit/1.4.0/*.aar