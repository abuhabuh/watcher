import Dependencies._

val akkaVersion = "2.5.4"

lazy val root = (project in file(".")).
  settings(
    inThisBuild(List(
      name := "watcher-scala",
      organization := "co.fabricsystems",
      scalaVersion := "2.12.3",
      version      := "0.0.2"
    )),

    // todo: move dependencies into Dependencies.scala and document
    libraryDependencies += scalaTest % Test,
    libraryDependencies ++= Seq(
      "com.typesafe.akka" %% "akka-actor" % akkaVersion,
      "com.typesafe.akka" %% "akka-remote" % akkaVersion,
      "com.typesafe.akka" %% "akka-cluster" % akkaVersion,
      "com.typesafe.akka" %% "akka-cluster-metrics" % akkaVersion,
      "com.typesafe.akka" %% "akka-cluster-tools" % akkaVersion,
      "com.typesafe.akka" %% "akka-multi-node-testkit" % akkaVersion
    ),
    libraryDependencies ++= Seq(
      "org.scalaj" %% "scalaj-http" % "2.3.0"
    )
  ).enablePlugins(JavaAppPackaging)

// todo: Doc where does packageName show up
packageName := "watcher-scala"
dockerRepository := Some("johnwang412")
dockerBaseImage := "anapsix/alpine-java:latest"
dockerUpdateLatest := true

