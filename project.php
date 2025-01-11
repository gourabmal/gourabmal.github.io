<?php include 'header.php'; ?>
<?php
$projectId = isset($_GET['id']) ? $_GET['id'] : null;

$projects = json_decode(file_get_contents('contents.txt'), true);

if ($projectId && isset($projects[$projectId])) {
    $project = $projects[$projectId];
} else {
    $project = null;
}
?>
<?php if ($project): ?>
  <section class="project-cs-hero">
    <div class="project-cs-hero__content">
      <h1 class="heading-primary"><?php echo htmlspecialchars($project['title']); ?></h1>
      <div class="project-cs-hero__info">
        <p class="text-primary">
        <?php echo nl2br(htmlspecialchars($project['short_description'])); ?>
        </p>
      </div>
      <div class="project-cs-hero__cta">
        <a href="<?php echo htmlspecialchars($project['project_link']); ?>" class="btn btn--bg" target="_blank" rel="noreferrer">Project
          Link</a>
      </div>
    </div>
  </section>
  <section class="project-details">
    <div class="main-container">
      <div class="project-details__content">
        <div class="project-details__showcase-img-cont">
          <img src="<?php echo htmlspecialchars($project['image']); ?>" alt="<?php echo htmlspecialchars($project['title']); ?>"class="project-details__showcase-img" />
        </div>
        <div class="project-details__content-main">
          <div class="project-details__desc">
            <h2 class="project-details__content-title">Project Overview</h2>
            <?php if (!empty($project['big_description_array'])): ?>
              <?php foreach ($project['big_description_array'] as $desc): ?>
                <p class="project-details__desc-para">
                <?php echo htmlspecialchars($desc); ?>
                </p>
              <?php endforeach; ?>
            <?php endif; ?>
          </div>
          <div class="project-details__tools-used">
          <?php if (!empty($project['tools_used'])): ?>
            <h2 class="project-details__content-title">Tools Used</h2>
            <div class="skills">
            <?php foreach ($project['tools_used'] as $tool): ?>
              <div class="skills__skill"><?php echo htmlspecialchars($tool); ?></div>
              <?php endforeach; ?>
            </div>
          <?php endif; ?>
          </div>
          <div class="project-details__links">
            <h2 class="project-details__content-title">See Live</h2>
            <a href="<?php echo htmlspecialchars($project['project_link']); ?>" class="btn btn--med btn--theme project-details__links-btn"
              target="_blank" rel="noreferrer">Project Link</a>
            <a href="./" class="btn btn--med btn--theme-inv project-details__links-btn">Go Back</a>
          </div>
        </div>
      </div>
    </div>
  </section>
<?php endif; ?>
<?php include 'footer.php'; ?>